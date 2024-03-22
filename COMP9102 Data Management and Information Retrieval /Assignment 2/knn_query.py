from datetime import datetime
import heapq
import math
import numpy as np
import time
import argparse

fname1 = 'data10K10.txt'
fname2 = 'queries10.txt'

def dist(p1, p2):
    ret = 0
    for e1, e2 in zip(p1, p2):
        ret += pow((e1-e2), 2)
    return math.sqrt(ret)

def get_pivots(data, numpivots):
    seed = data[0]
    maxdis = -1
    for i in range(len(data)):
        dis = dist(data[i], seed)
        if dis > maxdis:
            maxdis = dis
            pivots = [i]

    for _ in range(numpivots-1):
        maxdis = -1
        for o in range(len(data)):
            dis = sum([dist(data[p], data[o]) for p in pivots]) # cal dis between o and each p
            if dis > maxdis:
                p = o
                maxdis = dis
        pivots.append(p) # select farther o from pervious pivots
    
    diss = []
    for o in data:
        dis = []
        for p in pivots:
            dis.append(dist(o, data[p]))
        diss.append(dis)
    return pivots, diss

def npiv(oi, dist_o_p): # find the nearest pivot i
    dis = dist_o_p[oi]
    return dis.index(min(dis)), min(dis)

def cal_iDis(dist_o_p, numpivots):
    maxdi = [-1] * numpivots
    partition = [[] for _ in range(numpivots)]
    # record maxdi
    for oi in range(len(data)):
        i, di = npiv(oi, dist_o_p)
        partition[i].append(oi)
        if di > maxdi[i]:
            maxdi[i] = di
    return maxdi, partition

def naive(data, qs, k):
    time1 = time.time()
    res = []
    numcomp = 0
    for q in qs:
        pri_q = []
        for o in data:
            numcomp += 1
            pri_q.append(dist(q, o))
        d = heapq.nsmallest(k, pri_q)
        oi = map(pri_q.index, d)
        res.append({'dist': d, 'objs': list(oi)})
    time2 = time.time()
    return res, int(numcomp / len(qs)), time2-time1

def pivot(data, qs, numpivots, k):
    time1 = time.time()
    pivots, dist_o_p = get_pivots(data, numpivots)
    dist_p_q = []
    numcomp = 0
    for pi in pivots:
        tmp_dist = []
        for q in qs:
            numcomp += 1
            tmp_dist.append(dist(data[pi], q))
        dist_p_q.append(tmp_dist)

    res = []
    for qi, q in enumerate(qs):
        h = []
        for oi, o in enumerate(data):
            if len(h) < k:
                numcomp += 1
                heapq.heappush(h, (dist(q, o), oi)) # sort by dist
                h.sort()
            elif len(h) == k:
                prune = False
                eps = h[-1][0]
                for pidx, pi in enumerate(pivots):
                    if abs(dist_o_p[oi][pidx] - dist_p_q[pidx][qi]) > eps:
                        prune = True
                        break
                if not prune:
                    numcomp += 1
                    if dist(q, o) <= eps:
                        h[-1] = (dist(q, o), oi)
                        h.sort()
        res.append(h)
    time2 = time.time()
    return res, numcomp / len(qs), time2-time1

def iDistance(data, qs, numpivots, k):
    time1 = time.time()
    pivots, dist_o_p = get_pivots(data, numpivots)
    numcomp = 0
    maxdi, partition = cal_iDis(dist_o_p, numpivots)
    # calculate distance between q and pivots previously
    dist_q_p = []
    for q in qs:
        tmp_dist = []
        for pi in pivots:
            numcomp += 1
            tmp_dist.append(dist(q, data[pi]))
        dist_q_p.append(tmp_dist)

    res = []
    for qi, q in enumerate(qs):
        tmp_dist = dist_q_p[qi]
        i = tmp_dist.index(min(tmp_dist)) # nearest pivot to q
        ois = partition[i] # objects in the partition of pivot
        pri_q = []
        for oi in ois: # naive to find knn
            numcomp += 1
            heapq.heappush(pri_q, (dist(q, data[oi]), oi))
        pri_q.sort()
        knn = pri_q[:k]
        eps = knn[-1][0]
        for pidx, pi in enumerate(pivots): # remaining pivots
            if pidx == i: # jump nearest pivot
                continue
            if dist_q_p[qi][pidx] - maxdi[pidx] > eps: # prune
                continue
            for oi1 in partition[pidx]:
                numcomp += 1
                heapq.heappush(knn, (dist(q, data[oi1]), oi1))
            knn.sort()
            knn = knn[:k]
            
        res.append(knn)

    time2 = time.time()
    return res, numcomp / len(qs), time2-time1 

if __name__=="__main__":
    data = []
    with open(fname1, 'r') as f:
        for line in f:
            line = line.strip('\n').split()
            line = [float(i) for i in line]
            data.append(line)
    
    qs = []
    with open(fname2, 'r') as f:
        for line in f:
            line = line.strip('\n').split()
            line = [float(i) for i in line]
            qs.append(line)

    parser = argparse.ArgumentParser(description='Method Params')
    parser.add_argument('--numpivots', default=10, type=int, help='num of pivots')
    parser.add_argument('--k', default=5, type=int, help='K-Nearest Neighbor')
    args = parser.parse_args()

    # res, numcomp, time_consumed = naive(data, qs, args.k)
    # print(res)
    # print('average distance comp per query (Naive) =', numcomp)
    # print('total time Naive =', time_consumed)

    # res, numcomp, time_consumed = pivot(data, qs, args.numpivots, args.k)
    # # print(res)
    # print('average distance comp per query (Pivot-based) =', numcomp)
    # print('total time Pivot-based =', time_consumed)

    res, numcomp, time_consumed = iDistance(data, qs, args.numpivots, args.k)
    # print(res)
    print('average distance comp per query (iDistance) =', numcomp)
    print('total time iDistance =', time_consumed)
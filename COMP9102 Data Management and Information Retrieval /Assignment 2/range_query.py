from datetime import datetime
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

# find nearest pivot i and record dist(o, pi)
def npiv(oi, dist_o_p):
    dis = dist_o_p[oi]
    return dis.index(min(dis)), min(dis)

def cal_iDis(dist_o_p, numpivots):
    maxdi = [-1] * numpivots
    # record maxdi
    for oi in range(len(data)):
        i, di = npiv(oi, dist_o_p)
        if di > maxdi[i]:
            maxdi[i] = di
    maxd = max(maxdi)

    # calculate vo for each o
    iDis = []
    for oi in range(len(data)):
        i, di = npiv(oi, dist_o_p)
        vo = maxd * i + dist_o_p[oi][i]
        iDis.append(vo)
    sorted_iDis = sorted(enumerate(iDis), key=lambda x: x[1]) # sort by iDis
    return sorted_iDis, maxdi

def naive(data, qs, eps):
    time1 = time.time()
    res = []
    numcomp = 0
    for q in qs:
        for oi, o in enumerate(data):
            numcomp += 1
            if dist(q, o) <= eps:
                res.append(oi)
    time2 = time.time()
    return res, int(numcomp / len(qs)), time2-time1

def pivot(data, qs, numpivots, eps):
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
        for oi, o in enumerate(data):
            flag = True
            for pidx, pi in enumerate(pivots):
                if abs(dist_o_p[oi][pidx] - dist_p_q[pidx][qi]) > eps:
                    flag = False
                    break
            if flag:
                numcomp += 1
                if dist(q, o) <= eps:
                    res.append(oi)
    time2 = time.time()
    return res, numcomp / len(qs), time2-time1

def binary_search(iDis, l, r, low_bound):
    if r >= l:
        mid = int(l + (r - l)/2)
        if iDis[mid][1] > low_bound and iDis[mid-1][1] <= low_bound:
            return mid
        elif iDis[mid][1] > low_bound and iDis[mid-1][1] > low_bound:
            return binary_search(iDis, l, mid-1, low_bound)
        else: # iDis[mid][1] < low_bound
            return binary_search(iDis, mid+1, r, low_bound)
    else:
        return -1

def iDistance(data, qs, numpivots, eps):
    time1 = time.time()
    pivots, dist_o_p = get_pivots(data, numpivots)
    numcomp = 0
    iDis, maxdi = cal_iDis(dist_o_p, numpivots)
    maxd = max(maxdi)
    res = []
    for q in qs:
        for i, pi in enumerate(pivots):
            numcomp += 1
            tmp_dist = dist(q, data[pi])
            if tmp_dist - maxdi[i] > eps: # prune
                continue
            low_bound = maxd * i + tmp_dist - eps
            high_bound = maxd * i + tmp_dist + eps
            vi = binary_search(iDis, 0, len(iDis)-1, low_bound)
            if vi == -1:
                continue
            while vi < len(iDis) and iDis[vi][1] < high_bound:
                oi = iDis[vi][0]
                numcomp += 1
                if dist(q, data[oi]) <= eps:
                    res.append(oi)
                vi += 1
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
    parser.add_argument('--eps', default=0.2, type=float, help='distance bound')
    args = parser.parse_args()

    # res, numcomp, time_consumed = naive(data, qs, args.eps)
    # print(res)
    # print('average distance comp per query (Naive) =', numcomp)
    # print('total time Naive =', time_consumed)

    # res, numcomp, time_consumed = pivot(data, qs, args.numpivots, args.eps)
    # print(res)
    # print('average distance comp per query (Pivot-based) =', numcomp)
    # print('total time Pivot-based =', time_consumed)

    res, numcomp, time_consumed = iDistance(data, qs, args.numpivots, args.eps)
    print(res)
    print('average distance comp per query (iDistance) =', numcomp)
    print('total time iDistance =', time_consumed)
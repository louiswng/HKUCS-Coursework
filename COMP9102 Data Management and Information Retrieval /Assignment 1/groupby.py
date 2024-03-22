'''
1. read the entire files in data structures in memory.
2. sorted-merge
'''
import csv
import datetime
import pandas as pd

fname = 'data/R.tsv'
output = 'output/Rgroupby.tsv'

def MergeSort(lst):
    if len(lst) <= 1:
        return lst
    mid = int(len(lst)/2)
    left = MergeSort(lst[:mid])
    right = MergeSort(lst[mid:])
    return Merge(left, right)

def Merge(left, right):
    l, r = 0, 0
    result = []
    while l < len(left) and r < len(right):
        if left[l][0] < right[r][0]: # left < right
            result.append(left[l])
            l += 1
        elif left[l][0] == right[r][0]:
            tmp = left[l]
            tmp[1] += right[r][1]
            result.append(tmp)
            l += 1
            r += 1
        elif left[l][0] > right[r][0]:
            result.append(right[r])
            r += 1
    result += list(left[l:])
    result += list(right[r:])
    return result

print(datetime.datetime.now())

with open(output, 'w', newline='') as f:
    tsv_w = csv.writer(f, delimiter='\t')
    R = pd.read_csv(fname, sep='\t', header=None, names=['key', 'integer'], keep_default_na=False)
    R_dict = zip(R['key'], R['integer'])
    R_list = list(R_dict)
    R_list1 = []
    for elem in R_list:
        elem = list(elem)
        R_list1.append(elem)
    res = MergeSort(R_list1)
    tsv_w.writerows(res)
print(datetime.datetime.now())


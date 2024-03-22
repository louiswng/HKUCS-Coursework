import pandas as pd
import argparse
import heapq

file1 = '2017_TRB.csv'
file2 = '2017_AST.csv'
file3 = '2017_STL.csv'
file4 = '2017_BLK.csv'
file5 = '2017_PTS.csv'

parser = argparse.ArgumentParser()
parser.add_argument('--k', type=int, default="10", help="The number k of top players.")
parser.add_argument('--category_ids', nargs='?', default='[2,5]', help="The statistics categories that you are interested in.")
args = parser.parse_args()

ids = eval(args.category_ids)
files = []
col_names = []
for i in ids:
    if i == 1:
        files.append(pd.read_csv(file1, names=['rid', 'value']))
        col_names.append('TRB')
    elif i == 2:
        files.append(pd.read_csv(file2, names=['rid', 'value']))
        col_names.append('AST')
    elif i == 3:
        files.append(pd.read_csv(file3, names=['rid', 'value']))
        col_names.append('STL')
    elif i == 4:
        files.append(pd.read_csv(file4, names=['rid', 'value']))
        col_names.append('BLK')
    elif i == 5:
        files.append(pd.read_csv(file5, names=['rid', 'value']))
        col_names.append('PTS')

# normalize
for file in files:
    max_value = max(file['value'])
    file['value'] /= max_value

col_num = len(ids)
length = files[0].shape[0]
upper_bound = [0.0] * length
lower_bound = [0.0] * length
flags = [[False]*col_num for i in range(length)]
rid_set = set()
for i in range(length): # for each line of all files (columns)
    # 1. update upper & lower bound
    values = []
    for idx, file in enumerate(files):
        rid = file.iloc[i]['rid'].astype(int)
        value = file.iloc[i]['value']
        rid_set.add(rid)
        flags[rid][idx] = True # update flag array
        lower_bound[rid] += value # lower bound = lower bound + rid 对应
        values.append(value)
    upper_bound = lower_bound.copy()
    for rid in list(rid_set):
        for col in range(col_num):
            if not flags[rid][col]: # never seen
                upper_bound[rid] += values[col]
    # 2. caculate Wk
    if len(rid_set) <= args.k:
        continue
    Wk = heapq.nlargest(args.k, range(len(lower_bound)), lower_bound.__getitem__) # k objects with the largest lower bound
    smallest_rid = Wk[-1] # smallest lower bound in Wk
    obj_not_in_Wk = rid_set.difference(set(Wk))
    is_final = True
    for rid in list(obj_not_in_Wk):
        if upper_bound[rid] > lower_bound[smallest_rid]:
            is_final = False
    if is_final:
        break

print(Wk)
scores = [lower_bound[W] for W in Wk]
print(scores)
print(i)


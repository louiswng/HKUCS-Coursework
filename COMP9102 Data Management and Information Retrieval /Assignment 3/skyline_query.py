'''
1. read a line
2. judge p can be added in S
3. 
'''

import pandas as pd
import argparse

file = '2017_ALL.csv'

parser = argparse.ArgumentParser()
parser.add_argument('--category_ids', nargs='?', default='[2,5]', help="The statistics categories that you are interested in.")
args = parser.parse_args()
ids = eval(args.category_ids)
col_names = ['TRB', 'AST', 'STL', 'BLK', 'PTS']
drop_cols = []
select_cols = []
for i in range(5):
    if i+1 not in ids:
        drop_cols.append(col_names[i])
    else:
        select_cols.append(col_names[i])

data = pd.read_csv(file, sep=',', index_col=0).drop(columns=drop_cols)

def judgeDominated(pid1, pid2): # whether p1 is dominated by p2
    p1 = data.iloc[pid1-1]
    p2 = data.iloc[pid2-1]
    one_big = False
    for col in select_cols:
        if p1[col] > p2[col]:
            return False
        if p1[col] < p2[col]:
            one_big = True
    return one_big

S = []
for pid, p in data.iterrows(): # read a line
    if len(S) == 0:
        S.append(pid)
        continue
    dominated = False
    for playerid in S: # each player in S
        if judgeDominated(pid, playerid): # p dominated by player
            dominated = True
    if dominated: # p is ignored
        continue
    S.append(pid)
    remove_pids = []
    for playerid in S:
        if judgeDominated(playerid, pid): # player dominated by p, delete player from S
            remove_pids.append(playerid)
    for playerid in remove_pids:
        S.remove(playerid)
print(S)
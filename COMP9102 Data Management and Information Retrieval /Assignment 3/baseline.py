import pandas as pd
import argparse

file = '2017_ALL.csv'

parser = argparse.ArgumentParser()
parser.add_argument('--k', type=int, default="10", help="The number k of top players.")
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

scores = []
for idx, player in data.iterrows():
    score = 0
    for col in select_cols:
        score += player[col] / max(data[col])
    scores.append(score)
data['SCORE'] = scores
data = data.sort_values(by=['SCORE'], ascending=False)
print(data.head(args.k))

'''
1. lines should be read once only.
2. not read the entire files in data structures in memory. read each line and find results.
3. use buffer to record results of each line, do not need to read again when duplicate. record pervious line, buffer to record results
'''
import pandas as pd
import datetime

fname1 = 'data/R_sorted.tsv'
fname2 = 'data/S_sorted.tsv'
output = 'output/RjoinS.tsv'

R_sorted = pd.read_csv(fname1, sep='\t', header=None, names=['key', 'integer1'])
S_sorted = pd.read_csv(fname2, sep='\t', header=None, names=['key', 'integer2'])

res = R_sorted.join(S_sorted.set_index('key'), on='key')
res = res.astype({'integer2': 'int64'})

print(res.dtypes)
res['integer2'] = res['integer2'].astype('int64')
# res.to_csv(output, sep='\t')
# print(res)

print(datetime.datetime.now())

with open(output, 'w', newline='') as f:
    tsv_w = csv.writer(f, delimiter='\t')
    R = pd.read_csv(fname, sep='\t', header=None, names=['key', 'integer'])
    R = R.groupby(by=['key'], as_index=False, dropna=False).sum()
    
    for i in range(R.shape[0]):
        tsv_w.writerow([R['key'][i], R['integer'][i]])
print(datetime.datetime.now())
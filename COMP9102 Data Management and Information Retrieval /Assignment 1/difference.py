'''
1. lines should be read once only.
2. not read the entire files in data structures in memory.
3. no buffer.
4. eliminating duplicates.
'''
import csv
import datetime

fname1 = 'data/R_sorted.tsv'
fname2 = 'data/S_sorted.tsv'
output = 'output/RdifferenceS.tsv'

print(datetime.datetime.now())

f1 = open(fname1, 'r', encoding='utf-8')
line1_str = f1.readline()
line1 = line1_str.strip('\n').split('\t')
with open(output, 'w', newline='') as f, open(fname2, 'r', encoding='utf-8') as f2:
    tsv_w = csv.writer(f, delimiter='\t')
    preLine1, preLine2 = [None] * 2
    is_finished = False
    for line2 in f2:
        line2 = line2.strip('\n').split('\t')
        if preLine2 == line2: # duplicates
            continue
        while line1 <= line2:
            if line1 != line2:
                tsv_w.writerow(line1)
            preLine1 = line1
            line1_str = f1.readline()
            if not line1_str: # line1 is out
                is_finished = True
                break
            line1 = line1_str.strip('\n').split('\t')
            while line1 == preLine1:
                preLine1 = line1
                line1_str = f1.readline()
                line1 = line1_str.strip('\n').split('\t')

        if is_finished:
            break
        preLine2 = line2
f1.close()
print(datetime.datetime.now())
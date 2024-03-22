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
output = 'output/RintersectionS.tsv'

print(datetime.datetime.now())

f2 = open(fname2, 'r', encoding='utf-8')
line2 = f2.readline()
line2 = line2.strip('\n').split('\t')
with open(output, 'w', newline='') as f, open(fname1, 'r', encoding='utf-8') as f1:
    tsv_w = csv.writer(f, delimiter='\t')
    preLine1 = None
    for line1 in f1:
        line1 = line1.strip('\n').split('\t')
        if preLine1 == line1: # duplicates
            continue
        while line1 > line2:
            line2 = f2.readline()
            line2 = line2.strip('\n').split('\t')
        if line1 == line2: # intersect
            tsv_w.writerow(line1)
            line2 = f2.readline()
            line2 = line2.strip('\n').split('\t')
        preLine1 = line1
f2.close()
print(datetime.datetime.now())
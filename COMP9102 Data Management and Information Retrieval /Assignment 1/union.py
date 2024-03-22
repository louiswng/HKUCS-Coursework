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
output = 'output/RunionS.tsv'

print(datetime.datetime.now())

f1 = open(fname1, 'r', encoding='utf-8')
f2 = open(fname2, 'r', encoding='utf-8')
line1_str = f1.readline()
line2_str = f2.readline()
with open(output, 'w', newline='') as f:
    tsv_w = csv.writer(f, delimiter='\t')
    preline1, preline2 = [None] * 2
    while line1_str and line2_str:
        line1 = line1_str.strip('\n').split('\t')
        line2 = line2_str.strip('\n').split('\t')         
        while line1_str and preline1 == line1: # continue the next line if duplicates
            line1_str = f1.readline()
            line1 = line1_str.strip('\n').split('\t')
        while line2_str and preline2 == line2: # continue the next line if duplicates
            line2_str = f2.readline()
            line2 = line2_str.strip('\n').split('\t')
        if line1[0] < line2[0] or (line1[0] == line2[0] and line1[1] < line2[1]): # line1 < line2
            tsv_w.writerow(line1)
            preline1 = line1
            line1_str = f1.readline()
            line1 = line1_str.strip('\n').split('\t')
        elif line1 == line2: # line1 = line2
            tsv_w.writerow(line1)
            preline1 = line1
            preline2 = line2
            line1_str = f1.readline()
            line1 = line1_str.strip('\n').split('\t')
            line2_str = f2.readline()
            line2 = line2_str.strip('\n').split('\t')
        else: # line1 > line2
            tsv_w.writerow(line2)
            preline2 = line2
            line2_str = f2.readline()
            line2 = line2_str.strip('\n').split('\t')

    if line1_str: # output line1 and duplicate
        while line1_str:
            if line1 == preline1:
                line1_str = f1.readline()
                line1 = line1_str.strip('\n').split('\t')
                continue
            tsv_w.writerow(line1)
            preline1 = line1
            line1_str = f1.readline()
            line1 = line1_str.strip('\n').split('\t')

    if line2_str: # output line2 and duplicate
        while line2_str:
            if line2 == preline2:
                line2_str = f2.readline()
                line2 = line2_str.strip('\n').split('\t')
                continue
            tsv_w.writerow(line2)
            preline2 = line2
            line2_str = f2.readline()
            line2 = line2_str.strip('\n').split('\t')

f1.close()
f2.close()
print(datetime.datetime.now())
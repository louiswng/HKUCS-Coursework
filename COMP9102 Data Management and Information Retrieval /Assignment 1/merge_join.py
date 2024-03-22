'''
1. lines should be read once only.
2. not read the entire files in data structures in memory. read each line and find results.
3. when join attribute of the next line is the same as previous line in file1, use buffer to record lines in file2. no need to re-read file2
'''
import csv
import datetime

fname1 = 'data/R_sorted.tsv'
fname2 = 'data/S_sorted.tsv'
output = 'output/RjoinS.tsv'

print(datetime.datetime.now())

f2 = open(fname2, 'r', encoding='utf-8')
line2 = f2.readline()
line2 = line2.strip('\n').split('\t')
with open(output, 'w', newline='') as f, open(fname1, 'r', encoding='utf-8') as f1:
    tsv_w = csv.writer(f, delimiter='\t')
    preLine1, preBuffer = [None] * 2
    maxLen = 0
    for line1 in f1:
        line1 = line1.strip('\n').split('\t')
        if preLine1 is not None and preLine1[0] == line1[0]: # use previous result
            for pb in preBuffer:
                tsv_w.writerow([line1[0], line1[1], pb[1]])
            continue
        buffer = []
        while line1[0] > line2[0]:
            line2 = f2.readline()
            line2 = line2.strip('\n').split('\t')
        while line2[0] == line1[0]:
            buffer.append(line2)
            tsv_w.writerow([line1[0], line1[1], line2[1]])
            line2 = f2.readline()
            line2 = line2.strip('\n').split('\t')
        maxLen = len(buffer) if maxLen < len(buffer) else maxLen # update maxLen
        preLine1 = line1
        preBuffer = buffer
f2.close()
print(maxLen)
print(datetime.datetime.now())
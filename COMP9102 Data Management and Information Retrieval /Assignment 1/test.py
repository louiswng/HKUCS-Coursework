
fname = 'output/RdifferenceS.tsv'

with open(fname, 'r', encoding='utf-8') as f:
    preLine = None
    for line in f:
        line = line.strip('\n').split('\t')
        if preLine == line:
            print(line)
        preLine = line
data_path=./ModelNet10/bed/train/bed_0007.off
keep_proportion=0.9

python main.py \
    --data ${data_path} \
    --keep_proportion ${keep_proportion} \

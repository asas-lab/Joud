import json
import random

def stream_split_jsonl_file(input_file, train_file, val_file, val_ratio=0.2):
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(train_file, 'w', encoding='utf-8') as train_outfile, \
         open(val_file, 'w', encoding='utf-8') as val_outfile:

        for line in infile:
            if random.random() < val_ratio:
                # This line goes into the validation set
                val_outfile.write(line)
            else:
                # This line goes into the training set
                train_outfile.write(line)

# Usage
input_file = 'ar_hplt_full.json' # Replace with your JSON Lines file path
train_file = 'train.jsonl'
val_file = 'val.jsonl'

stream_split_jsonl_file(input_file, train_file, val_file, val_ratio=0.0015)

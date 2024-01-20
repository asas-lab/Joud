import json
import random

def get_args():
    # Create an argument parser to handle command-line arguments
    parser = argparse.ArgumentParser(description='Split your dataset into Train/Val.')

    parser.add_argument(
        '--input_file',
        type=str,
        help='Specify the path of the dataset that you want to split.'
    )
    parser.add_argument(
        '--train_file',
        type=str,
        default=None,
        help='The name of the generated train file.'
    )
    parser.add_argument(
        '--val_file',
        type=str,
        default=None,
        help='The name of the generated validation file.'
    )
    parser.add_argument(
        '--val_ratio',
        type=int,
        default=0.01,
        help='The validation percentage of the dataset.'
    )

    # Parse the command-line arguments
    args = parser.parse_args()
    return args


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

def main():

    args = get_args()
    stream_split_jsonl_file(args.input_file, args.train_file, args.val_file, args.val_ratio)

if __name__ == "__main__":
    main()

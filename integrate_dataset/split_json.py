import gzip
import argparse, logging


def get_args():
    Parser = argparse.ArgumentParser(description="Machine Translation Evalution")
    Parser.add_argument(
        '--source_file',
        type=str,
        help = 'the name or path of the model to use in the test.',
        required=True
    )
    Parser.add_argument(
        '--output_prefix',
        type=str,
        help = 'the prefix of files name',
    )
    Parser.add_argument(
        '--split_size',
         type=int,
          help = 'size of each split in MB',
       )
    args = Parser.parse_args()
    return args

def split_jsonl_gzip(source_file, prefix, max_size_mb):
    max_size_bytes = max_size_mb * 1024 * 1024
    current_size = 0
    count = 0
    out_file = gzip.open(f"{prefix}{count}.json.gz", 'wt')  # 'wt' for write text mode

    with open(source_file, 'r') as f:
        for line in f:
            if current_size + len(line) > max_size_bytes:
                out_file.close()
                count += 1
                out_file = gzip.open(f"{prefix}{count}.json.gz", 'wt')
                current_size = 0
            out_file.write(line)
            current_size += len(line)

    out_file.close()

if __name__ == "__main__":

    args = get_args()
    print(args)
    split_jsonl_gzip(source_file = args.source_file,
                    prefix = args.output_prefix,
                    max_size_mb = args.split_size)

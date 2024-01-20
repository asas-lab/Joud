import argparse, logging
from datasets import load_dataset
from tokenizers import ByteLevelBPETokenizer
from transformers import AutoConfig, AutoTokenizer

def get_args():
    Parser = argparse.ArgumentParser(description="Machine Translation Evalution")
    Parser.add_argument(
        '--ds_name_or_path',
        type=str,
        help = 'the name or path of the model to use in the test.',
        required=True
    )
    Parser.add_argument(
        '--subset',
        type=str,
        help = 'the name or path of the subset of the dataset to use in the test',
    )
    Parser.add_argument(
        '--cache_dir',
         type=str,
          help = 'The directory of the cache where the dataset is saved.',
       )
    Parser.add_argument(
        "--batch_size",
        type=int,
        default=1000,
        help='batch size'
    )
    Parser.add_argument(
        "--tokenizer_name_or_path",
        type=str,
        help='the name of the model configuration'
    )
    args = Parser.parse_args()
    return args


def main(argv):

    # Load Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_name_or_path,
                                              use_fast=True,)

    ext = args.ds_name_or_path.split('.')[-1]

    if ext in 'json':
        # Load the dataset
        ds= load_dataset(ext, data_files = args.ds_name_or_path, split='train', cache_dir=args.cache_dir)

    elif ext in 'py':
        
        ds= load_dataset(args.ds_name_or_path, split='train', cache_dir=args.cache_dir)

    else:
        ds = load_dataset(args.ds_name_or_path,args.subset,split='train', cache_dir=args.cache_dir)

    # Define a function to tokenize an example and return the number of tokens
    num_tokens = []
    # Define a function to tokenize an example and return the number of tokens
    def count_tokens(example):
        tokens = tokenizer(example['text'])['input_ids']
        num_token = [len(i) for i in tokens]
        num_tokens.append(sum(num_token))
        return example

    ds.map(count_tokens, batched=True)
    # Print the result
    print("The dataset contains", sum(num_tokens), "tokens.")



#if __name__ == '__main__':
args = get_args()

main(args)

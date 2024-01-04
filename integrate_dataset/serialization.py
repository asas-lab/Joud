from datasets import load_dataset
import argparse
import os
import warnings
"""
The code serializes the dataset into a specific format comprising of two columns:

1. text: This column include the raw text.
2. meta: This column includes all additional columns, along with the dataset name and subset name (if available).
"""
def get_args():
    # Create an argument parser to handle command-line arguments
    parser = argparse.ArgumentParser(description='Serialize metadata into a dataset.')

    parser.add_argument(
        '--dataset_name',
        type=str,
        help='Specify the name of the dataset that you want to modify.'
    )
    parser.add_argument(
        '--subset_name',
        type=str,
        default=None,
        help='Enter the subset name, if applicable, within the dataset.'
    )
    parser.add_argument(
        '--text_column',
        #type=str,
        nargs='+',
        default=['text'],
        help='Define the column name that contains the raw text.'
    )
    parser.add_argument(
        '--cache_dir',
        type=str,
        default=None,
        help='Provide the cache directory path for storing the dataset.'
    )
    parser.add_argument(
        '--save_path',
        type=str,
        help='Indicate the file path where the processed dataset will be saved.'
    )
    parser.add_argument(
        '--large',
        type=bool,
        default=False,
        help='Indicate the Weather the dataset is large (>10GB) or not.'
    )

    # Parse the command-line arguments
    args = parser.parse_args()
    return args

def serilization(ex,meta_col, ds_name, subset_name):
    """

    This function orgnize the columns of the datset to specific formats. it keeps the text_column
    and merge all the rest columns into new column name meta in dictonary format.
    The purpose is to consolidate metadata information within the dataset.

    Parameters:
        ex (dict): The input dictionary containing metadata.

    Returns:
        dict: The same input dictionary 'ex' after adding the 'meta' column.
    """

    meta = {i: ex[i] for i in meta_col}
    ex['meta'] = meta
    ex['meta']['dataset_name'] = ds_name
    if subset_name != None:
        ex['meta']['subset_name'] = subset_name

    return ex


def serilization_multi_col(ex,text_col,meta_col, ds_name, subset_name):

    meta = {i: ex[i] for i in meta_col}
    ex['meta'] = meta
    ex['meta']['dataset_name'] = ds_name
    if subset_name != None:
        ex['meta']['subset_name'] = subset_name

    ex['text'] = ', '.join(f"'{i}': '{ex[i]}'" for i in text_col)
    return ex


def main():


    args = get_args()

    ext = os.path.splitext(args.dataset_name)[-1][1:]

    if ext in ['json','csv','text']:
        ds = load_dataset(ext,
                          args.subset_name,
                          data_files=[args.dataset_name],
                          cache_dir=args.cache_dir)
        ds_name = os.path.splitext(args.dataset_name)[-2]
        subset_name = args.subset_name
    else:
        ds = load_dataset(args.dataset_name,
                          args.subset_name,
                          cache_dir=args.cache_dir)
        ds_name = args.dataset_name.split('/')[-1]
        subset_name = args.subset_name

    column_names = ds['train'].column_names

    if 'text' in column_names and 'text' not in args.text_column:
        ds = ds.rename_column('text', 'text1')
        column_names = ds['train'].column_names
    meta_columns = set(column_names) - set(args.text_column)

    if len(args.text_column) <2:

        text_column = args.text_column[0]


        # Call the serilization function with the input dictionary and the loaded dataset
        ds = ds.map(lambda ex: serilization(ex,meta_columns, ds_name, subset_name),
        remove_columns=meta_columns)
        #ds = ds.map(serilization, column_names, ds_name, subset_name)

        # make sure the raw text column named 'text':
        if text_column != 'text':
            ds = ds.rename_column(text_column, 'text')


    else:
        ds = ds.map(lambda ex: serilization_multi_col(ex,args.text_column,meta_columns, ds_name, subset_name),
        remove_columns=column_names)

    if not args.large:
        if 'validation' in list(ds.column_names.keys()):
            ds['validation'].to_json(f'{args.save_path}/ar_{ds_name}_val.json',
                        lines=True,
                        force_ascii=False)

        else:
            ds = ds.train_test_split(test_size=0.01)
            ds['test'].to_json(f'{args.save_path}/ar_{ds_name}_val.json',
                        lines=True,
                        force_ascii=False)

        # Save the dataset into jsonl
        ds['train'].to_json(f'{args.save_path}/ar_{ds_name}.json',
                    lines=True,
                    force_ascii=False)

    else:
        ds['train'].to_json(f'{args.save_path}/ar_{ds_name}.json',
                    lines=True,
                    force_ascii=False)
if __name__ == "__main__":
    warnings.warn("Please assign --large to True if your dataset is bigger than 10 GB The test_train_split function in huggingface dataset consume large time to save the file in json format if you do spliting to large dataset.")
    main()

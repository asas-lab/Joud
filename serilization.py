from datasets import load_dataset
import argparse
"""
The code serializes the dataset into a specific format comprising of two columns:

1. text: This column include the raw text.
2. meta: This column includes all additional columns, along with the dataset name and subset name (if available).
"""
def get_args():
    # Create an argument parser to handle command-line arguments
    parser = argparse.ArgumentParser(description='Serialize metadata into a dataset.')

    parser.add_argument(
        'dataset_name',
        type=str,
        help='Name of the dataset to modify'
    )
    parser.add_argument(
        'subset_name',
        type=str,
        default=None,
        help='Name of the subset if needed'
    )
    parser.add_argument(
        'text_column',
        type=str,
        default='text',
        help='Name of the text column'
    )
    parser.add_argument(
        'cache_dir',
        type=str,
        default=None,
        help='Cache path where the dataset is going to be cached.'
    )
    parser.add_argument(
        'save_path',
        type=str,
        help='The path of the dataset to be saved'
    )

    # Parse the command-line arguments
    args = parser.parse_args()
    return args

def serilization(ex):
    """

    This function orgnize the columns of the datset to specific formats. it keeps the text_column
    and merge all the rest columns into new column name meta in dictonary format.
    The purpose is to consolidate metadata information within the dataset.

    Parameters:
        ex (dict): The input dictionary containing metadata.

    Returns:
        dict: The same input dictionary 'ex' after adding the 'meta' column.
    """

    meta_col = set(ds['train'].column_names) - set(config.text_column)
    meta = {i: ex[i] for i in meta_col}
    ex['meta'] = meta
    ex['meta']['dataset_name'] = ds_name

    return ex

def main():


    args = get_args()

    if ext in ['json','csv','text']
        ds = load_dataset(ext,
                          args.subset,
                          data_files=[args.dataset_name],
                          cache_dir=args.cache_dir)

    else:
        ds = load_dataset(args.dataset_name,
                          args.subset,
                          cache_dir=args.cache_dir)

    # Call the serilization function with the input dictionary and the loaded dataset
    ds = ds.map(serilization)

    # make sure the raw text column named 'text':
    if config.text_column != 'text':
        ds = ds.rename_column(config.text_column, 'text')

    # Save the dataset into jsonl
    ds.to_json(args.save_path,
                lines=True,
                force_ascii)


if __name__ == "__main__":
    main()

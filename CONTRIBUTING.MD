# CONTRIBUTING

# What is Joud?

Content is under development

### Quick-Start Guide to contribute in Joud

Steps to add new datasets to the Joud Huggingface Repository:

1. Initiate or Claim a Pull Request (PR):

    Open a PR to propose the addition of a new dataset to Joud, or claim claim an existing open PR.


2. Convert Dataset to JSON Lines Format:

    Run the script Joud/integrate_dataset/serialization.py to convert a dataset (either stored in HuggingFace or locally) into JSON lines format. Execute the script using the following command:

```
python serialization.py \
  --dataset_name dataset_name_or_path \
  --subset_name dataset_subset_name_if_exist \
  --text_column the_name_of_raw_text_column \
  --cache_dir cache_path_name \
  --save_path save_file_path \
  --large True \
```

    The output is a .json file containing two columns: text and meta. The text column contains the raw text, while meta includes all additional columns. For datasets with multiple text columns, list them in the --text_column argument, i.e : `--text_column col1_name col2_name ...`

3. Generate Training and Validation Splits:

    Use the generate_val.py script to divide the dataset into training and validation subsets:

```
python generate_val.py \
  --input_file dataset_path \
  --train_file trainset_path_to_be_saved \
  --val_file validation_path_to_be_saved \
  --val_ratio split_percentage \
```

4. Split and Compress JSON Files:

    Run the split_json.sh script to divide the JSON file into smaller segments and then compress them:

```
./split_json.sh MAX_SIZE source.json prefix_
```

    Set `MAX_SIZE` to "1024" which denotes to the maximum size of each json file.
    The `source.json` parameters determine the json file that will be splited and compressed.
    The `prefix_` denotes to the prefix for each file, e.g., `ar_datasetname_`

5. Test the Dataset:

    Validate the dataset by executing the `test_ds.py` script. If the dataset passes the test successfully, it is ready for upload to HuggingFace. Remember to update the ds_dataloader script by modifying the `_Path` variable accordingly.

  ```
  python test_ds.py  
  ```


6. Token Count Calculation:

    Determine the number of tokens in each dataset using the `num_tokens.py` script. This script employs the BPE tokenizer for token calculation. Please report the number of tokens in the PR.

```
python num_tokens.py  \
    --tokenizer_name_or_path khalidalt/tokenizer_bpe \
    --ds_name_or_path json_file_path_or_ds_loader_py_path \
```

Important Note on Dataset Upload:

    When uploading the dataset to HuggingFace, please use Git instead of the push_to_hub method. This is crucial to maintain the file extension dataset_name.json.gz as it is.


Your participation and contributions are immensely valued in the ongoing development and expansion of Joud.

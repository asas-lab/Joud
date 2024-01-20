from datasets import load_dataset


ds = load_dataset('ds_dataloader.py',
                    cache_dir='cache/')

print("Dataset has been successfully load")

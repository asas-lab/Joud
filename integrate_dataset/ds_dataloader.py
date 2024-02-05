"""This script test that your dataset has been convert into correct .json.gz format."""

"""

## How to test this script ?
## run the following lines in jypter or in python script.
from datasets import load_dataset
ds = load_dataset('Path-to-ds_dataloader/ds_dataloader.py')

"""
import gzip
import json
import datasets
import glob

name = 'DatasetTet'

logger = datasets.logging.get_logger(name)


_DESCRIPTION = """\
"""

_CITATION = """

"""

_Path = "/ar_*.json.gz"




class DatasetTest(datasets.GeneratorBasedBuilder):
    """"""



    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "text": datasets.Value("string"),
                    'meta': datasets.Value("string"),

                }
            ),
            supervised_keys=None,
            homepage=_Path,
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepaths": glob.glob(_Path)}),

        ]

    def _generate_examples(self, filepaths):
        """This function returns the examples in the raw (text) form by iterating on all the files."""
        id_ = 0
        for filepath in filepaths:

            logger.info("generating examples from = %s", filepath)
            with gzip.open(open(filepath, "rb"), "rt", encoding="utf-8") as f:
                for line in f:
                    if line:
                        example = json.loads(line)


                        yield id_, {'text': example['text'], 'meta': example['meta']}
                        id_ += 1

#!/bin/bash
# run this script using the following command line: 
# chmod +x ./split_json.sh
# ./split_json.sh [number_of_lines] [your_data.json] [ar_datasetname_]
# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 [NUMBER_OF_LINES] [SOURCE_FILE] [PREFIX]"
    exit 1
fi

NUMBER_OF_LINES=$1
SOURCE_FILE=$2
PREFIX=$3

# Split the file
split -l $NUMBER_OF_LINES -d --additional-suffix=.json $SOURCE_FILE ${PREFIX}

# Rename the first file (if it exists) to remove the leading zero
if [ -f "${PREFIX}00.json" ]; then
    mv "${PREFIX}00.json" "${PREFIX}0.json"
fi

# Rename the remaining files
a=1
for i in ${PREFIX}0*; do 
  if [ -f "$i" ]; then
    mv "$i" "${PREFIX}$a.jsonl"
    let a=a+1
  fi
done

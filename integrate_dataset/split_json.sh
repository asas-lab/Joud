#!/bin/bash

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
a=0
for i in ${PREFIX}*; do 
  if [ -f "$i" ]; then
    mv "$i" "${PREFIX}$a.json"
    let a=a+1
  fi
done


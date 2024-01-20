#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 [MAX_SIZE_MB] [SOURCE_FILE] [PREFIX]"
    exit 1
fi

MAX_SIZE_MB=$1
SOURCE_FILE=$2
PREFIX=$3
MAX_SIZE_BYTES=$((MAX_SIZE_MB * 1024 * 1024))

# Function to split the JSON file
split_json() {
    local file=$1
    local prefix=$2
    local max_size=$3
    local current_size=0
    local count=0
    local out_file="${prefix}${count}.json"

    while IFS= read -r line; do
        local size=$(echo "$line" | wc -c)
        if (( current_size + size > max_size )); then
            count=$((count + 1))
            out_file="${prefix}${count}.json"
            current_size=0
        fi
        echo "$line" >> "$out_file"
        current_size=$((current_size + size))
    done < "$file"
}

# Call the function
split_json "$SOURCE_FILE" "$PREFIX" "$MAX_SIZE_BYTES"

# Compress the files
gzip ${PREFIX}*.json

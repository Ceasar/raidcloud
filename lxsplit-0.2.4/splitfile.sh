#!/bin/sh

# splitfile.sh: reliably splits a given file into n equal* pieces
# * the last file probably won't be the samme size as the others, 

size=$(ls -l "$1" | awk '{ print $5}')
echo "File $1 is $size bytes"
numparts=$2
chunksize=$(( ($size/$numparts) + 1 ))
chunksizehuman=$(echo "$chunksize" | bc)

echo "Splitting file into $2 parts of size $chunksizehuman bytes each"

./lxsplit -s "$1" "$chunksize"b
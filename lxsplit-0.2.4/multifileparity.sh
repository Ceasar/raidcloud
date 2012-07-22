#!/bin/sh

# multifileparity: 
# usage: ./multifileparity [OUTFILE] [FILES ...]

echo $1
echo $2

out="$1"

# the first file is our starting point
cp "$(echo $2)" "$(echo $out)"

# cuts out our output and first file from the args, 
# so our loop loops over the files we want
shift 2

for file in "$@"
do
  ./fileparity "$file" "$out" > ./tempparity
  mv -f ./tempparity "$out"
done
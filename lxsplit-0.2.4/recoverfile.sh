#!/bin/sh

# recovers a part file based on the original filename and the missing part number
# usage: ./recoverfile.sh [FILE] [XXX]

IFS=$'\n'
files=$(ls -1 ../tmp/ | grep -E "$1.(par|[0-9]{3})")

out="$1"."$2"
cp ../tmp/$( echo "$files" | head -1 ) "$out"

for f in $( echo "$files" | tail +1 )
do
  #echo $f
  ./fileparity ../tmp/"$f" "$out" > ./tempparity
  mv -f ./tempparity "$out"
done

mv "$out" ../tmp/
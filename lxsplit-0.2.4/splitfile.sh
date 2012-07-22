#!/bin/sh

# splitfile.sh: reliably splits a given file into n equal* pieces
# * the last file probably won't be the samme size as the others, 
# but we pad it with null terminators to force it to be equal


# grab the size of the inputted file
sizetext=$(ls -l "$1")
size=$( echo $sizetext | awk '{ print $5}')
#echo "File $1 is $size bytes"
numparts=$2

# calculate the proper chunk size to create the requested number of pieces
chunksize=$(echo "($size+$numparts-1)/$numparts" | bc)
#echo $otherchunk
#chunksize=$(( ($size/$numparts) + 1 ))
chunksizehuman=$(echo "$chunksize" | bc)

#echo "Splitting file $1 into $2 parts of size $chunksizehuman bytes each"

./lxsplit -s "$1" "$chunksize"b > /dev/null

# delete the original file
rm "$1"

# find out which part file is the last one, so we can calculate how much we need to pad
files=$(ls -1 | grep "$1")
lastfile=$( echo "$files" | tail -1 )

lastfilesize=$(ls -l "$lastfile" | awk '{ print $5}')

#echo "last file size: $lastfilesize"

numpadbytes=$((chunksizehuman - lastfilesize))
#echo "Padding $lastfile with $numpadbytes bytes"

for i in $(seq 1 1 $numpadbytes)
do
  printf '\0' >> $lastfile
done

args=""
IFS=$'\n'
out="$1".par
cp $( echo "$files" | head -1 ) "$out"
for f in $( echo "$files" | tail +1 )
do
  ./fileparity "$f" "$out" > ./tempparity
  mv -f ./tempparity "$out"
done

# make parity file
#./multifileparity.sh "$1".par $args

echo "$numpadbytes"
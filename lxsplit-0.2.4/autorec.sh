#!/bin/sh

# automatically figures out which file needs to be recovered, and recovers it
# takes original file name and total expected chunks as input
# dies if there's more than one file missing
# usage: ./autorec.sh [FILE] [NUMFILES]

files=$(ls -1 ../tmp/ | grep -E "$1.([0-9]{3})")

for i in $( seq 1 $2 ) 
do 
   line="$1."$(printf "%03d" "$i")
   line=$(echo $line)
   expectedfiles=$line'\n'$expectedfiles
done

#echo $expectedfiles
#echo $files
missing=$(echo "$expectedfiles$files" | sort | uniq -u)
if [ "$missing" = "" ]
then
    echo "No files are missing, congrats"
else
    echo "$missing is missing"
    if [ $(echo "$missing" | wc -l) -gt 1 ]
    then
	echo "more than one file missing, I can't help you"
    else
	./recoverfile.sh "$1" "$missing"
	echo "recovered $missing"
    fi
fi
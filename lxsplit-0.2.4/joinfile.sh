#!/bin/sh

SCRIPT=$(readlink -f $0)
SCRIPTPATH=$(dirname $SCRIPT)
fname=$(basename "$1")

firstfile=$(ls "$1".* | head -1)

./lxsplit -j "$firstfile"
mv ./"$fname" ../tmp/

#this doesn't work reliavly
./autotrunc "$1"


#if [ "$2" -gt 0 ]
#then
  #size=$(ls -l "$1" | awk '{ print $5}')
  #newsize=$(($size-$2))
  #echo "Truncating $2 bytes"
  #./truncate "$1" $newsize
#fi
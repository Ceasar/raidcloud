#!/bin/sh

firstfile=$(ls "$1".* | head -1)

./lxsplit -j "$firstfile"

if [ $2 -gt 0 ]
then
  size=$(ls -l "$1" | awk '{ print $5}')
  newsize=$(($size-$2))
  echo "Truncating $2 bytes"
  ./truncate "$1" $newsize
fi
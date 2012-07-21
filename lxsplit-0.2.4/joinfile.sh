#!/bin/sh

firstfile=$(ls "$1" | head -1)

./lxsplit -j "$firstfile"
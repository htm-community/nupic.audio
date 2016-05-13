#!/bin/bash

root=$PWD/../..
dataDirs="data/training-a
data/training-b
data/training-c
data/training-d
data/training-e"
destDir="$root/data/normals"
classType="RECORDS-normal"

mkdir -p $destDir
for p in $dataDirs; do
  for r in `cat $root/$p/$classType`; do
    #ls -l $root/$p/${r}".wav"
    cp -a $root/$p/${r}".wav" $destDir
    echo "\"$root/$p/${r}\"," >> normals.csv
  done
done

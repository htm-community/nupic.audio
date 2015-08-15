#!/bin/bash

if [ "${#}" -lt "1" ]
  then
  echo "Generate various train and test sets from the syllables database"
  echo "Creates files in the current directory: train_speakers and test_speakers"
  echo "for training and testing."
  echo "Usage $0 train_set [value]"
  echo "  Where train_set is one of"
  echo "  ring: train on all syllabes from a given ring of points, value: 1-7"
  echo "    (1 is the outermost ring, 7 is the innermost (original) ring)"
#  echo "  spoke: train on  all syllabes on a given spoke, value: 1-8"
#  echo "  random: a randomly distributed set of syllabes from across all"
#  echo "    training points"
  exit -1
fi

# Names of various files and directories. 
# Rename here if you don't like them for some reason.
WORK=work
SYLLIST=syls
TRAIN_LIST=train_speakers
TEST_LIST=test_speakers

if [ $1 == "ring" ]
  then
  if [ "$#" -lt "2" ] 
    then
    RING=7
  else
    RING=$2
  fi
  exec 3> $WORK/$TRAIN_LIST
  exec 5> $WORK/$TEST_LIST
  for r in {1..7}
  do
    for s in {1..8}
    do
      if [ "$RING" -eq "$r" ]
        then
          echo "`./spoke_point.sh $s $r`" >&3
        else
          echo "`./spoke_point.sh $s $r`" >&5
      fi
    done
  done
fi

exec 3>&-
exec 5>&-

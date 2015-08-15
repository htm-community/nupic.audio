#!/bin/bash
# Generate training and testing scripts for HTK
# 
# First argument is a string: "inner_talkers" train on the inner circle of talkers
#                             "outer_talkers" train on the outer circle of talkers
# Second argument is the directory in which to place output files
# Third argument is the name of the features directory
# Fourth argument is the feature name
#
# File generated are: training_master_label_file, testing_master_label_file,
# training_script, testing_script
set -e 
set -u

TALKERS=$1
WORK=$2
FEATURES_DIR=$3
FEATURE_NAME=$4

TRAIN_MLF=training_master_label_file
TEST_MLF=testing_master_label_file
TRAIN_SCRIPT=training_script
TEST_SCRIPT=testing_script
SYLLIST=syllable_list

BASEDIR=`dirname $0`

if [ $TALKERS == "inner_talkers" ]; then
    $BASEDIR/train_on_central.sh $WORK/training_talkers $WORK/testing_talkers
fi

if [ $TALKERS == "outer_talkers" ]; then
    $BASEDIR/train_on_extrema.sh $WORK/training_talkers $WORK/testing_talkers
fi

# In general, we want to do our testing on all the talkers (training talkers and
# testing talkers) so the train and test talkers are combined here to make a single
# testing set.
cat $WORK/training_talkers $WORK/testing_talkers > $WORK/all_talkers

# The vowels and consonants that make up the CNBH database
VOWELS="a e i o u"
CONSONANTS="b d f g h k l m n p r s t v w x y z"
SILENCE="sil"

# Generate a temporary list of the sylables in the database
if [ -a $WORK/$SYLLIST.tmp ] 
then
  rm $WORK/$SYLLIST.tmp
fi

echo "Generating temporary syllable list..."
for v in $VOWELS; do
  echo $v$v >> $WORK/$SYLLIST.tmp
  for c in $CONSONANTS; do
    echo $v$c >> $WORK/$SYLLIST.tmp
    echo $c$v >> $WORK/$SYLLIST.tmp
  done
done

# Sort the syllable list and delete the 
# temporary, unsorted version
sort $WORK/$SYLLIST.tmp > $WORK/$SYLLIST
rm $WORK/$SYLLIST.tmp

# Construct the conversion scripts for AIMCopy (or HCopy) and 
# the master label files for the train and test sets
echo "Generating master label files..."
if [ -a $WORK/$TRAIN_MLF ]
then
  rm $WORK/$TRAIN_MLF
fi
if [ -a $WORK/$TEST_MLF ]
then
  rm $WORK/$TEST_MLF
fi
exec 4> $WORK/$TRAIN_MLF
exec 6> $WORK/$TEST_MLF
echo '#!MLF!#' >&4
echo '#!MLF!#' >&6

for syllable in $(cat $WORK/${SYLLIST}); do
  for speaker in $(cat $WORK/training_talkers); do
    DEST_FILENAME=$FEATURES_DIR/$syllable/${syllable}${speaker}
    echo "'\"${DEST_FILENAME}.lab\"'" >&4
    echo "$SILENCE" >&4
    echo $syllable >&4
    echo "$SILENCE" >&4
    echo "." >&4
  done
  for speaker in $(cat $WORK/all_talkers); do
    DEST_FILENAME=$FEATURES_DIR/$syllable/${syllable}${speaker} 
    echo "'\"${DEST_FILENAME}.lab\"'" >&6
    echo "$SILENCE" >&6
    echo $syllable >&6
    echo "$SILENCE" >&6
    echo "." >&6
  done
done
exec 4>&-
exec 6>&-

echo "Generating train and test scripts..."
if [ -a $WORK/$TRAIN_SCRIPT ]
then
  rm $WORK/$TRAIN_SCRIPT
fi
if [ -a $WORK/$TEST_SCRIPT ]
then
  rm $WORK/$TEST_SCRIPT
fi  
exec 7> $WORK/$TRAIN_SCRIPT
exec 8> $WORK/$TEST_SCRIPT
for syllable in $(cat $WORK/${SYLLIST}); do
  for speaker in $(cat $WORK/training_talkers); do
    DEST_FILENAME=$FEATURES_DIR/$syllable/${syllable}${speaker}
    echo "'${DEST_FILENAME}.${FEATURE_NAME}'" >&7
  done
  for speaker in $(cat $WORK/all_talkers); do
    DEST_FILENAME=$FEATURES_DIR/$syllable/${syllable}${speaker}
      echo "'${DEST_FILENAME}.${FEATURE_NAME}'" >&8
  done
done
exec 7>&-
exec 8>&-

rm $WORK/${SYLLIST}
# Note: don't delete 'all_talkers', 'training_talkers' or 'testing_talkers' because
# they're used later by the plotting scripts.



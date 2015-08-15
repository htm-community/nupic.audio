#!/bin/bash
# Script to run a single HMM train/test cycle with the given parameters.
# This script expects the following variables to be set
#
# total_hmm_states - total number of HMM states (including the 2 non-emitting states)
# mixture_components - number of components in the output distribution for each emitting state
# input_vector_size - number or elements in the input vector (normally 39 for MFCCs, 12 for AIM)
# feature_code - HTK feature type code for the features being used (normally MFCC_0_D_A for MFCCs and USER_E_D_A for AIM features)
# FEATURE_SUFFIXES - List of suffixes appended to the feature filenames. For the MFCCs this is just "mfc" but for the AIM feature, there can be multiple features generated from each run of AIMCopy
# WORKING_DIRECTORY - working directory
# SYLLIST_COMPLETE

set -e
set -u

# Filenames generated here

# This must be named 'proto' to keep HCompV happy.
HMMPROTO=proto
HHED_SCRIPT=hhed_change_components_script
RECOUT=recognition_output
RESULTS_FILE=results
MISCLASSIFIED=misclassified_syllables

# Filenames used here
#TRAIN_SCRIPT=training_script
#TEST_SCRIPT=testing_script
SYLLIST_COMPLETE=syllable_list_with_silence
#TEST_MLF=testing_master_label_file

DICT=dictionary
WDNET=word_network

SILENCE=sil

THIS_DIR=`dirname $0`

hmm_type=${total_hmm_states}_states_${mixture_components}_mixture_components
echo "HMM type: ${hmm_type}..."

if [ -e $WORKING_DIRECTORY/$hmm_type/.hmm_success ]; then
  echo " already done"
  return 0
fi

mkdir -p $WORKING_DIRECTORY/$hmm_type

echo "Creating HMM structure..."
$THIS_DIR/gen_hmmproto.py --input_size ${input_vector_size} --total_hmm_states ${total_hmm_states} --feature_type ${feature_code} > $WORKING_DIRECTORY/$hmm_type/$HMMPROTO

echo "Adding output mixture components..."
$THIS_DIR/gen_hhed_script.py --num_means ${mixture_components} --total_hmm_states ${total_hmm_states} > $WORKING_DIRECTORY/$hmm_type/$HHED_SCRIPT


echo "Training HMM..."
echo "Setting up prototype HMM..."
mkdir -p $WORKING_DIRECTORY/$hmm_type/hmm0
HCompV -C $WORKING_DIRECTORY/$HMMCONFIG -f 0.01 -m -S $TRAIN_SCRIPT -M $WORKING_DIRECTORY/$hmm_type/hmm0 $WORKING_DIRECTORY/$hmm_type/$HMMPROTO

echo "Generating HMM definitions..."
# Now take the prototype file from hmm0, and create the other HMM definitions
# from it
grep -A 9999 "<BEGINHMM>" $WORKING_DIRECTORY/$hmm_type/hmm0/$HMMPROTO > $WORKING_DIRECTORY/$hmm_type/hmm0/hmms
if [ -e $WORKING_DIRECTORY/$hmm_type/hmm0/hmmdefs ]; then
  rm $WORKING_DIRECTORY/$hmm_type/hmm0/hmmdefs
fi
for syllable in $(cat $WORKING_DIRECTORY/$SYLLIST_COMPLETE); do
  echo "~h $syllable" >> $WORKING_DIRECTORY/$hmm_type/hmm0/hmmdefs
  cat $WORKING_DIRECTORY/$hmm_type/hmm0/hmms >> $WORKING_DIRECTORY/$hmm_type/hmm0/hmmdefs
done

echo -n "~o<STREAMINFO> 1 ${input_vector_size}<VECSIZE> ${input_vector_size}<NULLD><${feature_code}><DIAGC>" > $WORKING_DIRECTORY/$hmm_type/hmm0/macros

cat $WORKING_DIRECTORY/$hmm_type/hmm0/vFloors >> $WORKING_DIRECTORY/$hmm_type/hmm0/macros

HHEd -H $WORKING_DIRECTORY/$hmm_type//hmm0/macros -H $WORKING_DIRECTORY/$hmm_type/hmm0/hmmdefs $WORKING_DIRECTORY/$hmm_type/$HHED_SCRIPT $WORKING_DIRECTORY/$SYLLIST_COMPLETE

for iter in $TRAINING_ITERATIONS_LIST; do
  echo "Training iteration ${iter}..."
  let "nextiter=$iter+1"
  if [ ! -d $WORKING_DIRECTORY/$hmm_type/hmm$nextiter ]; then
    mkdir $WORKING_DIRECTORY/$hmm_type/hmm$nextiter
    HERest -C $WORKING_DIRECTORY/$HMMCONFIG -I $TRAIN_MLF \
      -t 250.0 150.0 1000.0 -S $TRAIN_SCRIPT \
      -H $WORKING_DIRECTORY/$hmm_type/hmm$iter/macros -H $WORKING_DIRECTORY/$hmm_type/hmm$iter/hmmdefs \
      -M $WORKING_DIRECTORY/$hmm_type/hmm$nextiter $WORKING_DIRECTORY/$SYLLIST_COMPLETE
  fi
done

for iter in $TESTING_ITERATIONS_LIST; do
  echo "Testing iteration ${iter}..."
  if [ ! -f $WORKING_DIRECTORY/$hmm_type/${RESULTS_FILE}_iteration_$iter ]; then
    HVite -H $WORKING_DIRECTORY/$hmm_type/hmm$iter/macros -H $WORKING_DIRECTORY/$hmm_type/hmm$iter/hmmdefs \
      -C $WORKING_DIRECTORY/$HMMCONFIG -S $TEST_SCRIPT -i $WORKING_DIRECTORY/$hmm_type/$RECOUT \
      -w $WORKING_DIRECTORY/$WDNET -p 0.0 -s 5.0 $WORKING_DIRECTORY/$DICT $WORKING_DIRECTORY/$SYLLIST_COMPLETE
    echo "Results from testing on iteration ${iter}..."
    HResults -e "???" ${SILENCE} -I $TEST_MLF $WORKING_DIRECTORY/$SYLLIST_COMPLETE $WORKING_DIRECTORY/$hmm_type/$RECOUT
    HResults -p -t -e "???" ${SILENCE} \
      -I $TEST_MLF $WORKING_DIRECTORY/$SYLLIST_COMPLETE $WORKING_DIRECTORY/$hmm_type/$RECOUT > $WORKING_DIRECTORY/$hmm_type/${RESULTS_FILE}_iteration_$iter
  fi
  # Count the number of instances of each talker appearing in the list of errors.
  grep Aligned $WORKING_DIRECTORY/$hmm_type/${RESULTS_FILE}_iteration_$iter| sed -E "s/.*\/..\/([a-z]{2})([0-9]{2,3}\.[0-9])p([0-9]{2,3}\.[0-9])s.*/\2p\3s/" | sort | uniq -c > $WORKING_DIRECTORY/$hmm_type/${MISCLASSIFIED}_iteration_$iter
  python ./cnbh-syllables/results_plotting/gen_results.py --input_file=$WORKING_DIRECTORY/$hmm_type/${MISCLASSIFIED}_iteration_$iter --train_talkers=$WORKING_DIRECTORY/training_talkers --test_talkers=$WORKING_DIRECTORY/testing_talkers --spoke_pattern=$SPOKE_PATTERN_FILE > $WORKING_DIRECTORY/$hmm_type/results_iteration_${iter}.txt
  python ./cnbh-syllables/results_plotting/spider_plot.py --input_file=$WORKING_DIRECTORY/$hmm_type/results_iteration_${iter}.txt --output_file=$WORKING_DIRECTORY/$hmm_type/results_iteration_${iter}.pdf
done
touch $WORKING_DIRECTORY/$hmm_type/.hmm_success



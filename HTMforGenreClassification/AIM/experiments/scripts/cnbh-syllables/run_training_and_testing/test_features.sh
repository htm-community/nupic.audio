#!/bin/bash
#
# Train and test an HTK monophone model using AIM or MFCC
# features and the CNBH syllable databse
#
# Copyright 2009-2010 University of Cambridge
# Author: Thomas Walters <tom@acousticscale.org>
#
# Run multiple HMMs

set -e
set -u

WORKING_DIRECTORY=$1
FEATURE_SOURCE=$2
FEATURE_SUFFIX=$3
HMM_STATES_LIST=$4
MIXTURE_COMPONENTS_LIST=$5
TRAINING_ITERATIONS_LIST=$6
TESTING_ITERATIONS_LIST=$7
input_vector_size=$8
feature_code=$9
TRAIN_SCRIPT=${10}
TEST_SCRIPT=${11}
TRAIN_MLF=${12}
TEST_MLF=${13}
SPOKE_PATTERN_FILE=${14}

HMMCONFIG=hmm_configuration

THIS_DIR=`dirname $0`

if [ "$feature_code" == "MFCC_0_D_A" ]
then
  cat <<"EOF" > $WORKING_DIRECTORY/$HMMCONFIG
# Coding parameters
SOURCEFORMAT= HTK
EOF
else
  cat <<"EOF" > $WORKING_DIRECTORY/$HMMCONFIG
# Coding parameters
# The TARGETKIND and SOURCEKIND lines are to add deltas and delta-deltas to
# the AIM features
SOURCEFORMAT= HTK
SOURCEKIND= USER_E
TARGETKIND = USER_E_D_A
EOF
fi

for total_hmm_states in $HMM_STATES_LIST; do
  for mixture_components in $MIXTURE_COMPONENTS_LIST; do
    . $THIS_DIR/run_test_instance.sh &
    #. $THIS_DIR/run_test_instance.sh
  done
done
echo "Waiting..."
wait


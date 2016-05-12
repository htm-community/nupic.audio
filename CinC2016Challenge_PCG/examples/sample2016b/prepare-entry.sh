#!/bin/bash
#
# file: prepare-entry.sh
#
# This script shows how to run the example code (setup.sh and next.sh)
# over the validation set, in order to produce the list of expected
# answers (answers.txt) which must be submitted as part of your entry.
# This script itself does not need to be included in your entry.

set -e
set -o pipefail

echo "==== training model ===="

octave -q -f --eval "
  pkg load signal;
  schmidt_options = default_Schmidt_HSMM_options;
  load('example_data.mat');
  train_recordings = example_data.example_audio_data([1:5]);
  train_annotations = example_data.example_annotations([1:5],:);
  [B_matrix, pi_vector] = trainSchmidtSegmentationAlgorithm(train_recordings, train_annotations, schmidt_options.audio_Fs, false);
  save 'example_model.mat' B_matrix pi_vector;
"

echo "==== running setup script ===="

./setup.sh

echo "==== running entry script on validation set ===="

rm -f answers.txt
# use GNU parallel if available
if parallel -k </dev/null >/dev/null 2>/dev/null; then
    parallel -k --halt=1 < validation/RECORDS \
        echo {} \; ln -sf validation/{}.wav . \; ./next.sh {}
else
    for r in `cat validation/RECORDS`; do
        echo $r
        ln -sf validation/$r.wav .
        ./next.sh $r
    done
fi

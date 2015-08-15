#!/bin/bash
# Copyright 2009-2010 Thomas Walters <tom@acousticscale.org>
# 
# Add pink noise to the CNBH syllables database. The first argument is the
# path to the clean .wav files. The second argument is a quoted list of the 
# desired SNRs in dB, separated by spaces. Directories are made for each SNR
# in the directory above that given in the first argument.
set -e
set -u

CLEAN_SYLLABLES_DATABASE_PATH=$1
SIGNAL_TO_NOISE_RATIOS=$2

# The syllables database is approximately at -9dB re. the max RMS level for a
# .wav file.
REFERENCE_SIGNAL_LEVEL="-9"
SAMPLE_RATE=48000

PREV_DIR=`pwd`
cd $CLEAN_SYLLABLES_DATABASE_PATH

for SNR in ${SIGNAL_TO_NOISE_RATIOS}; do
  echo "Generating noisy data for SNR ${SNR}dB"
  if [ ! -e ../snr_${SNR}dB/.pink_noise_success ]
  then
    mkdir -p ../snr_${SNR}dB/
    VOWELS="a e i o u"
    CONSONANTS="b d f g h k l m n p r s t v w x y z"
    for v in $VOWELS; do
      mkdir ../snr_${SNR}dB/$v$v
      for c in $CONSONANTS; do
        mkdir ../snr_${SNR}dB/$c$v
        mkdir ../snr_${SNR}dB/$v$c
      done
    done
    NOISE_LEVEL=$(( $REFERENCE_SIGNAL_LEVEL - $SNR ))
    for file in `find . -iname "*.wav"`; do
      # Note: the 0.684 below is the length of each syllable in the database
      # in seconds
      sox -r ${SAMPLE_RATE} -b 16 -n -t s2 - synth 0.684 pinknoise vol ${NOISE_LEVEL} dB | sox -m -v 0.25 $file -t s2 -r ${SAMPLE_RATE} -c 1 - ../snr_${SNR}dB/${file}
    done
    touch ../snr_${SNR}dB/.pink_noise_success
  fi
done
cd $PREV_DIR
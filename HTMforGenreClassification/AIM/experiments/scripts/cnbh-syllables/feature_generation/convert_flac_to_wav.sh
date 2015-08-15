#!/bin/bash
# Copyright 2009-2010 Thomas Walters <tom@acousticscale.org>
#
# Makes a copy of the cnbh syllables database in FLAC format found in
# $SOUNDS_ROOT/cnbh-syllables. The database is uncompressed to .WAV format
# for use with AIMCopy and HCopy.
# The first command-line argument is the location of $SOUNDS_ROOT
set -e
set -u

SOUNDS_ROOT=$1

if [ ! -e $SOUNDS_ROOT/clean/.make_clean_wavs_success ]; then
  mkdir -p $SOUNDS_ROOT/clean
  VOWELS="a e i o u"
  CONSONANTS="b d f g h k l m n p r s t v w x y z"
  for v in $VOWELS; do
    mkdir -p $SOUNDS_ROOT/clean/$v$v
    for c in $CONSONANTS; do
      mkdir -p $SOUNDS_ROOT/clean/$c$v
      mkdir -p $SOUNDS_ROOT/clean/$v$c
    done
  done
  CURRENT_DIR=`pwd`
  cd $SOUNDS_ROOT/cnbh-syllables/
  for file in `find . -iname "*.flac"`; do
    sox $file ../clean/${file%flac}wav
  done
  touch $SOUNDS_ROOT/clean/.make_clean_wavs_success
  cd $CURRENT_DIR
fi
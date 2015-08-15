#!/bin/bash
#
# Create HTK grammar and other files for the CNBH syllables database.
#
# Copyright 2009-2010 Thomas Walters <tom@acousticscale.org>
#
# The first command-line argument is the directory in which to place
# the generated files.
#
# The following files are generated:
# grammar - HTK grammar file
# dictionary - HTK dictionary file
# syllable_list_with_silence - As above, with a silence syllable appended
# word_network - Word network, as generated with HParse

# TODO(tom): check for empty $1 and make WORK="."
WORK=$1

# Generated filenames
GRAM=grammar
DICT=dictionary
SYLLIST_COMPLETE=syllable_list_with_silence
WDNET=word_network

# The vowels and consonants that make up the CNBH database
VOWELS="a e i o u"
CONSONANTS="b d f g h k l m n p r s t v w x y z"
SILENCE="sil"

# Make the sets of VC, CV, and vowel only labels, plus silence and use them to
# generate the grammar, dictionary and list of syllables
if [ -a $WORK/$SYLLIST_COMPLETE.tmp ] 
then
  rm $WORK/$SYLLIST_COMPLETE.tmp
fi

if [ -a $WORK/$DICT.tmp ] 
then
  rm $WORK/$DICT.tmp
fi

echo "Generating grammar, dictionary and syllable list..."
echo -n '$word = ' > $WORK/$GRAM
FIRST=true;
for v in $VOWELS; do
  echo "$v$v [$v$v] $v$v" >> $WORK/$DICT.tmp
  echo $v$v >> $WORK/$SYLLIST_COMPLETE.tmp
  if $FIRST; then
    echo -n "$v$v" >> $WORK/$GRAM
    FIRST=false
  else
    echo -n " | $v$v" >> $WORK/$GRAM
  fi
  for c in $CONSONANTS; do
    echo "$v$c [$v$c] $v$c" >> $WORK/$DICT.tmp 
    echo -n " | $v$c" >> $WORK/$GRAM
    echo "$c$v [$c$v] $c$v" >> $WORK/$DICT.tmp 
    echo -n " | $c$v" >> $WORK/$GRAM
    echo $v$c >> $WORK/$SYLLIST_COMPLETE.tmp
    echo $c$v >> $WORK/$SYLLIST_COMPLETE.tmp
  done
done
echo ';' >> $WORK/$GRAM

# Sort the dictionary and delete the 
# temporary, unsorted version
sort $WORK/$DICT.tmp > $WORK/$DICT
rm $WORK/$DICT.tmp

# Sort the syllable list and delete the 
# temporary, unsorted version
sort $WORK/$SYLLIST_COMPLETE.tmp > $WORK/$SYLLIST_COMPLETE
rm $WORK/$SYLLIST_COMPLETE.tmp

# Add silence to the end of the various files just generated
echo $SILENCE >> $WORK/$SYLLIST_COMPLETE
echo "end_$SILENCE [$SILENCE] $SILENCE" >> $WORK/$DICT
echo "start_$SILENCE [$SILENCE] $SILENCE" >> $WORK/$DICT
echo "(  start_$SILENCE   \$word   end_$SILENCE  )" >> $WORK/$GRAM

# Use HParse to parse the grammar into a wordnet
echo "Generating wordnet from grammar..."
${HTK_PREFIX}HParse $WORK/$GRAM $WORK/$WDNET




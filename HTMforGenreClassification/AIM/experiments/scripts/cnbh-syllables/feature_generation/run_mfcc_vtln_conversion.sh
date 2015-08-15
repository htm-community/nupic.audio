#!/bin/bash
# 
HCOPY_CONFIG=hcopy.config
HCOPY=`which HCopy`
if [ "$HCOPY" == "" ]; then
  echo "Please build HTK and make the binaries available in the path"
fi

set -e
set -u

FEATURES_DIR=$1
SOUND_SOURCE=$2

FULL_LIST=feature_generation_script

# Temporary file names
SYLLIST=syllable_list
TALKERS=talker_list

# The vowels and consonants that make up the CNBH database
VOWELS="a e i o u"
CONSONANTS="b d f g h k l m n p r s t v w x y z"

if [ ! -e $FEATURES_DIR/.features_script_success ]; then
mkdir -p $FEATURES_DIR

# Make the sets of VC, CV, and vowel only labels, plus silence and use them to
# generate the grammar, dictionary and list of syllables
if [ -a $FEATURES_DIR/$SYLLIST.tmp.tmp ] 
then
  rm $FEATURES_DIR/$SYLLIST.tmp.tmp
fi

for v in $VOWELS; do
  echo $v$v >> $FEATURES_DIR/$SYLLIST.tmp.tmp
  for c in $CONSONANTS; do
    echo $v$c >> $FEATURES_DIR/$SYLLIST.tmp.tmp
    echo $c$v >> $FEATURES_DIR/$SYLLIST.tmp.tmp
  done
done

# Sort the syllable list and delete the 
# temporary, unsorted version
sort $FEATURES_DIR/$SYLLIST.tmp.tmp > $FEATURES_DIR/$SYLLIST.tmp
rm $FEATURES_DIR/$SYLLIST.tmp.tmp

cat <<"EOF" > $FEATURES_DIR/${TALKERS}.tmp
170.9p112.2s
171.0p112.8s	
171.3p111.7s	
171.5p113.1s	
171.9p111.5s	
172.1p113.0s	
172.4p111.9s	
172.5p112.5s
171.7p112.3s	
137.0p104.3s	
141.3p135.4s	
145.5p106.3s	
148.8p128.8s	
151.6p83.9s	
153.0p108.1s	
155.5p123.5s	
156.7p90.6s	
159.5p109.6s	
161.1p119.4s	
161.1p96.8s	
163.4p157.6s	
164.7p110.8s	
164.9p102.1s	
165.6p144.0s	
165.7p116.2s	
167.4p133.5s	
167.8p106.5s	
168.6p111.6s	
168.9p125.4s	
169.0p114.0s	
170.0p109.7s	
170.1p119.5s	
171.0p115.5s	
172.4p109.3s	
173.3p105.6s	
173.5p115.0s	
174.5p100.6s	
174.5p110.6s	
174.9p113.0s	
175.7p118.5s	
176.1p94.5s	
178.0p108.5s	
178.1p87.6s	
178.8p123.6s	
179.0p113.9s	
180.4p80.1s	
183.0p105.7s	
183.0p130.4s	
184.8p115.1s	
188.1p139.2s	
189.6p102.1s	
192.7p116.7s	
194.5p150.4s	
198.1p97.9s	
202.7p118.6s	
208.6p93.2s	
215.2p121.0s
EOF


# Make the necessary directories for the computed features
echo "Making directory structure..."
for syllable in $(cat $FEATURES_DIR/${SYLLIST}.tmp); do
  mkdir -p $FEATURES_DIR/$syllable
done

echo "Creating HCopy config file..."
cat <<"EOF" > $FEATURES_DIR/${HCOPY_CONFIG}
# Coding parameters
SOURCEFORMAT= WAV
TARGETKIND = MFCC_0_D_A
TARGETRATE = 100000.0
SAVECOMPRESSED = T
SAVEWITHCRC = T
WINDOWSIZE = 250000.0
USEHAMMING = T
PREEMCOEF = 0.97
NUMCHANS = 200
CEPLIFTER = 22
NUMCEPS = 12
ENORMALISE = F
# Parameters a bit like Welling and Ney (2002)
# Can't do zero, it seems.
WARPLCUTOFF = 10 
# Upper frequency is the Nyquist freq. (24000Hz) 
# so choose the break freq. close to that
#WARPUCUTOFF = 23000
WARPUCUTOFF = 10500
EOF

for TALKER in $(cat $FEATURES_DIR/${TALKERS}.tmp); do
  echo "Generating script..."
  exec 3> $FEATURES_DIR/${FULL_LIST}_$TALKER
  for syllable in $(cat $FEATURES_DIR/${SYLLIST}.tmp); do
    SOURCE_FILENAME=$SOUND_SOURCE/$syllable/${syllable}${TALKER}.wav
    DEST_FILENAME=$FEATURES_DIR/$syllable/${syllable}${TALKER}.htk
    echo "$SOURCE_FILENAME  ${DEST_FILENAME}" >&3
  done
  exec 3>&-
  cp $FEATURES_DIR/${HCOPY_CONFIG} $FEATURES_DIR/${HCOPY_CONFIG}_$TALKER
  scale=`echo $TALKER | sed 's/.*p//' | sed 's/s.*//'`
  warpfactor=0`echo "scale=4; 100.0/$scale" | bc`
  echo "WARPFREQ = $warpfactor" >> $FEATURES_DIR/${HCOPY_CONFIG}_$TALKER
  HCopy -T 1 -C $FEATURES_DIR/${HCOPY_CONFIG}_$TALKER -S $FEATURES_DIR/${FULL_LIST}_$TALKER
done

#echo "Waiting for tasks to complete..."
#wait
#echo "Done!"

rm $FEATURES_DIR/$SYLLIST.tmp
rm $FEATURES_DIR/${TALKERS}.tmp
touch $FEATURES_DIR/.features_script_success
fi

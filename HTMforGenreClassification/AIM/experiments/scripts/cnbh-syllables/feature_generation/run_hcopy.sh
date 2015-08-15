#!/bin/bash

HCOPY=`which HCopy`
if [ "$HCOPY" == "" ]; then
  echo "Please build HTK and make the binaries available in the path"
fi

set -e
set -u

FEATURES_DIR=$1
MACHINE_CORES=$2
FILE_LIST=feature_generation_script
HCOPY_CONFIG=hcopy_configuration

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
# WARPLCUTOFF = 10 
# Upper frequency is the Nyquist freq. (24000Hz) 
# so choose the break freq. close to that
# WARPUCUTOFF = 23000
EOF

echo "Splitting data files over cores..."
total_cores=$(($MACHINE_CORES))
echo -n $total_cores
echo " cores available"
total_files=`cat $FEATURES_DIR/$FILE_LIST | wc -l | sed 's/ *//'`
echo -n $total_files
echo " files to process"
files_per_core=$(($total_files/$total_cores+1))
echo -n $files_per_core
echo " files per core"
split -l $files_per_core $FEATURES_DIR/$FILE_LIST $FEATURES_DIR/split_list
splits=( $(ls $FEATURES_DIR/split_list*))
element=0
echo -n "Spawning "
echo -n $total_cores
echo " tasks..."
for ((c=1;c<=$MACHINE_CORES;c+=1)); do
  s=${splits[$element]}
  HCopy -T 1 -C $FEATURES_DIR/${HCOPY_CONFIG} -S $s &
  let element=element+1
done

echo "Waiting for tasks to complete..."
wait
echo "Done!"
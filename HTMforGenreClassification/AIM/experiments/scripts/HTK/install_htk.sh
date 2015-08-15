#!/bin/bash
set -e
set -u
WORKING=$1
PREV_DIR=`pwd`
if [ ! -e $WORKING/.htk_installed_success ]; then
mkdir -p $WORKING
cd $WORKING
wget --user $HTK_USERNAME --password $HTK_PASSWORD http://htk.eng.cam.ac.uk/ftp/software/HTK-3.4.1.tar.gz
tar -xzf HTK-3.4.1.tar.gz
cd htk
./configure --disable-hslab
make
sudo make install
touch $WORKING/.htk_installed_success
fi
cd $PREV_DIR

#!/bin/bash
# Run ami-2fc2e95b (32 bit) or ami-05c2e971 (64 bit) in eu-west zone 
# ec2-run-instances  --user-data-file ec2_user_data.sh --key tom_eu_west --instance-type m1.small --instance-count 1 --region eu-west-1 --availability-zone eu-west-1b ami-2fc2e95b
# ec2-run-instances --user-data-file ec2_user_data.sh --key tom_eu_west --instance-type c1.xlarge --instance-count 1 --region eu-west-1 --availability-zone eu-west-1b ami-05c2e971
su ubuntu
sudo apt-get -y update
sudo apt-get -y install bc subversion scons pkg-config libsndfile1-dev build-essential libboost-dev python sox python-matplotlib

# For 64-bit systems, uncomment this line:
sudo apt-get -y install libc6-dev-i386

sudo mkdir -p /mnt/aimc
sudo chown `whoami` /mnt/aimc
sudo mkdir -p /mnt/log
sudo chown `whoami` /mnt/log
cd /mnt/aimc
svn checkout http://aimc.googlecode.com/svn/trunk/ aimc-read-only
cd aimc-read-only/experiments/scripts/
./master.sh &> /mnt/log/log.log

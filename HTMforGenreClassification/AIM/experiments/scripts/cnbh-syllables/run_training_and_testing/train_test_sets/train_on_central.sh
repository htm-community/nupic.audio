#!/bin/bash
# Copyright 2010 Thomas Walters 
#
# Generate a list of filenames from the syllables spoke pattern.
# The first argument is the filname for the training talkers, the second
# argument is the filename for the testing talkers.

TRAIN_TALKERS=$1
TEST_TALKERS=$2

# Training talkers are the central talker and the 8 talkers around the
# central ring closest to the central talker.
cat <<"EOF" > $TRAIN_TALKERS
170.9p112.2s
171.0p112.8s	
171.3p111.7s	
171.5p113.1s	
171.9p111.5s	
172.1p113.0s	
172.4p111.9s	
172.5p112.5s
171.7p112.3s	
EOF

# Testing talkers are all other talkers in the spoke pattern.
cat <<"EOF" > $TEST_TALKERS
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

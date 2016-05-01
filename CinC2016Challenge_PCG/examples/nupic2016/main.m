%% PREPROCESS DATA
clc; clear; close all
!./preprocess.sh
wav2vect
train = csvread('train.csv');
pcg=train(:,2);
pcg_full = csvread('signal.csv');
pcg_full = pcg_full(:,2);

%% TRAIN HTM model
enc_min = min(pcg_full) % use these to set params of nupic encoder!
enc_max = max(pcg_full)
enc_resol = mean(abs(diff(pcg_full))) %TODO improve this

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

%add header
!echo "reset,consumption" > training/tr.csv
!echo "int,float" >> training/tr.csv
!echo "R," >> training/tr.csv
!cat train.csv >> training/tr.csv

% run HTM model
!python run_opf_experiment.py -c trained training/
!python run_opf_experiment.py --load trained training/

%% EVALUATE/CLASSIFY

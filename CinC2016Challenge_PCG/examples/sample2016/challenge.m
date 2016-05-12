function classifyResult = challenge(recordName)
%
% Sample entry for the 2016 PhysioNet/CinC Challenge.
%
% INPUTS:
% recordName: string specifying the record name to process
%
% OUTPUTS:
% classifyResult: integer value where
%                     1 = abnormal recording
%                    -1 = normal recording
%                     0 = unsure (too noisy)
%
% To run your entry on the entire training set in a format that is
% compatible with PhysioNet's scoring enviroment, run the script
% generateValidationSet.m
%
% The challenge function requires that you have downloaded the challenge
% data 'training_set' in a subdirectory of the current directory.
%    http://physionet.org/physiobank/database/challenge/2016/
%
% This dataset is used by the generateValidationSet.m script to create
% the annotations on your training set that will be used to verify that
% your entry works properly in the PhysioNet testing environment.
%
%
% Version 1.0
%
%
% Written by: Chengyu Liu, Fubruary 21 2016
%             chengyu.liu@emory.edu
%
% Last modified by: Chengyu Liu, April 3 2016
%             Note: using 'audioread' to replace the 'wavread' function to load the .wav data.
%
%

%% Load the trained parameter matrices for Springer's HSMM model.
% The parameters were trained using 409 heart sounds from MIT heart
% sound database, i.e., recordings a0001-a0409.
load('Springer_B_matrix.mat');
load('Springer_pi_vector.mat');
load('Springer_total_obs_distribution.mat');

%% Load data and resample data
springer_options   = default_Springer_HSMM_options;
[PCG, Fs1]         = audioread([recordName '.wav']);  % load data
PCG_resampled      = resample(PCG,springer_options.audio_Fs,Fs1); % resample to springer_options.audio_Fs (1000 Hz)

%% Running runSpringerSegmentationAlgorithm.m to obtain the assigned_states
[assigned_states] = runSpringerSegmentationAlgorithm(PCG_resampled, springer_options.audio_Fs, Springer_B_matrix, Springer_pi_vector, Springer_total_obs_distribution, false); % obtain the locations for S1, systole, s2 and diastole

%% Running extractFeaturesFromHsIntervals.m to obtain the features for normal/abnormal heart sound classificaiton
features  = extractFeaturesFromHsIntervals(assigned_states,PCG_resampled);

%% Running classifyFromHsIntervals.m to obtain the final classification result for the current recording
classifyResult = classifyFromHsIntervals(features);

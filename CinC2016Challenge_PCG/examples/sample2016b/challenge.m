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
% Last modified by:
%
%

%% Load the trained parameter matrices for Springer's HSMM model.
load('example_model.mat');

%% Load data and resample data
schmidt_options    = default_Schmidt_HSMM_options;
[PCG, Fs1, nbits1] = wavread([recordName '.wav']);  % load data
PCG_resampled      = resample(PCG,schmidt_options.audio_Fs,Fs1); % resample to schmidt_options.audio_Fs (1000 Hz)

%% Running runSchmidtSegmentationAlgorithm.m to obtain the assigned_states
[assigned_states] = runSchmidtSegmentationAlgorithm(PCG_resampled, schmidt_options.audio_Fs, B_matrix, pi_vector, false); % obtain the locations for S1, systole, s2 and diastole

%% Running extractFeaturesFromHsIntervals.m to obtain the features for normal/abnormal heart sound classificaiton
features  = extractFeaturesFromHsIntervals(assigned_states,PCG_resampled);

%% Running classifyFromHsIntervals.m to obtain the final classification result for the current recording
classifyResult = classifyFromHsIntervals(features);

%%
clc; clear; close all
%% Load the trained parameter matrices for Springer's HSMM model.
% The parameters were trained using 409 heart sounds from MIT heart
% sound database, i.e., recordings a0001-a0409.
cd examples/sample2016/
load('Springer_B_matrix.mat');
load('Springer_pi_vector.mat');
load('Springer_total_obs_distribution.mat');
springer_options   = default_Springer_HSMM_options;
springer_options.audio_Fs = 30 %TODO subsample to which value? (higher=longer learning, lower=worse data)
cd ../..

%% Load data and resample data
normals = importfile('normals.csv');
result=[];
for i=1:size(normals)
    r=normals{i};
    r=r(2:end-1)
    [PCG, Fs1] = audioread([r '.wav']);  % load data
    PCG_resampled = resample(PCG,springer_options.audio_Fs,Fs1); % resample to springer_options.audio_Fs (1000 Hz)
    reset = zeros(size(PCG_resampled),1);
    reset(1)=1; %construct reset column for HTM
    result = [result; [reset PCG_resampled]];
end
plot(result(:,2));
%% store
csvwrite('train.csv',result);

%%

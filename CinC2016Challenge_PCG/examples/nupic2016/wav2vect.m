%% Load the trained parameter matrices for Springer's HSMM model.
% The parameters were trained using 409 heart sounds from MIT heart
% sound database, i.e., recordings a0001-a0409.
load('Springer_B_matrix.mat');
load('Springer_pi_vector.mat');
load('Springer_total_obs_distribution.mat');
springer_options   = default_Springer_HSMM_options;
springer_options.audio_Fs = 1000 %TODO subsample to which value? (higher=longer learning, lower=worse data)

%% Load data and resample data
normals = importfile('normals.csv');
N=size(normals)
prob=0.01; % to make this faster, use only random 2\% of the files; %FIXME process all files
result=[]; % select signal/features used for training
signal=[]; % whole PCG signal, unprocessed
for i=1:N
    r=normals{i};
    r=r(2:end-1);
    [PCG, Fs1] = audioread([r '.wav']);  % load data
    PCG_resampled = resample(PCG,springer_options.audio_Fs,Fs1); % resample to springer_options.audio_Fs (1000 Hz)
    
    reset = zeros(size(PCG_resampled),1);
    reset(1)=1; %construct reset column for HTM
    signal = [signal; [reset PCG_resampled]]; % store complete signal

    if(rand > prob) 
        continue; %skip
    end
    
    ['At ',num2str(i),' of ',num2str(N),' file: ',r]
   
    % Running runSpringerSegmentationAlgorithm.m to obtain the assigned_states
    [assigned_states] = runSpringerSegmentationAlgorithm(PCG_resampled, springer_options.audio_Fs, Springer_B_matrix, Springer_pi_vector, Springer_total_obs_distribution, false); % obtain the locations for S1, systole, s2 and diastole
    % use only S1, S2
    FHS=PCG_resampled(assigned_states==1 | assigned_states==2);
    %FIXME NuPIC We dont use features:  Running extractFeaturesFromHsIntervals.m to obtain the features for normal/abnormal heart sound classificaiton
    %features  = extractFeaturesFromHsIntervals(assigned_states,PCG_resampled);
    %FIXME NUPIC we ideally would use whole PCG_resampled
    
    reset = zeros(size(FHS),1);
    reset(1)=1; %construct reset column for HTM
    result = [result; [reset FHS]];
end

%plot(result(:,2));
%% store
csvwrite('train.csv',result);
csvwrite('signal.csv',signal);
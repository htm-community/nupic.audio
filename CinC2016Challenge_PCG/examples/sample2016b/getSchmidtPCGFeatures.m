% function [PCG_Features, featuresFs] = getSchmidtPCGFeatures(audio, Fs, figures)
%
% Get the features used in the Schmidt segmentation algorithm. This is only
% the homomorphic envelope of the signal, downsampled to 50hz
%
%% INPUTS:
% audio_data: array of data from which to extract features
% Fs: the sampling frequency of the audio data
% figures (optional): boolean variable dictating the display of figures
%
%% OUTPUTS:
% PCG_Features: array of derived features
% featuresFs: the sampling frequency of the derived features. This is set
% in default_Schmidt_HSMM_options.m
%
% This code is derived from the paper:
% S. E. Schmidt et al., "Segmentation of heart sound recordings by a 
% duration-dependent hidden Markov model," Physiol. Meas., vol. 31,
% no. 4, pp. 513-29, Apr. 2010.
%
% Developed by David Springer for comparison purposes in the paper:
% D. Springer et al., ?Logistic Regression-HSMM-based Heart Sound 
% Segmentation,? IEEE Trans. Biomed. Eng., In Press, 2015.
%
%% Copyright (C) 2016  David Springer
% dave.springer@gmail.com
% 
% This program is free software: you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation, either version 3 of the License, or
% any later version.
% 
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
% GNU General Public License for more details.
% 
% You should have received a copy of the GNU General Public License
% along with this program.  If not, see <http://www.gnu.org/licenses/>.

function [PCG_Features, featuresFs] = getSchmidtPCGFeatures(audio_data, Fs, figures)

if(nargin < 3)
    figures = false;
end

schmidt_options = default_Schmidt_HSMM_options;

featuresFs = schmidt_options.audio_segmentation_Fs; % Downsampled feature sampling frequency

%% 25-400Hz 4th order Butterworth band pass
audio_data = butterworth_low_pass_filter(audio_data,2,400,Fs, false);
audio_data = butterworth_high_pass_filter(audio_data,2,25,Fs);

%% Spike removal from the original paper:
audio_data = schmidt_spike_removal(audio_data,Fs);

%% Find the homomorphic envelope
homomorphic_envelope = Homomorphic_Envelope_with_Hilbert(audio_data, Fs);

%% Downsample the envelope:
downsampled_homomorphic_envelope = resample(homomorphic_envelope,featuresFs, Fs);

%% normalise the envelope:
downsampled_homomorphic_envelope = normalise_signal(downsampled_homomorphic_envelope);

PCG_Features = [downsampled_homomorphic_envelope];


%% Plotting figures
if(figures)
    figure('Name', 'PCG Features');
    t1 = (1:length(audio_data))./Fs;
    plot(t1,audio_data);
    hold on;
    t2 = (1:length(PCG_Features))./featuresFs;
    plot(t2,PCG_Features,'r');
    legend('Original Signal', 'Derived features');
    pause();
end
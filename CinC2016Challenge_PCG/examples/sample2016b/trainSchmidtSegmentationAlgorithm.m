% function [B_matrix, pi_matrix] = trainSchmidtSegmentationAlgorithm(PCGCellArray, annotationsArray, Fs, figures)
%
% Training the emissions matrix, B_matrix, and initial distribution,
% pi_vector, for the Schmidt HMM segmentation algorithm.
%
%% Inputs:
% PCGCellArray: A 1XN cell array of the N audio signals. For evaluation
% purposes, these signals should be from a distinct training set of
% recordings, while the algorithm should be evaluated on a separate test
% set of recordings, which are recorded from a completely different set of
% patients (for example, if there are numerous recordings from each
% patient).
% annotationsArray: a Nx2 cell array: position (n,1) = the positions of the
% R-peaks and postion (n,2) = the positions of the end-T-waves
% (both in SAMPLES)
% Fs: The sampling frequency
% figures (optional): boolean variable dictating the disaplay of figures.
%
%% Outputs:
% The B_matrix and pi arrays for an HMM - as Schmidt et al's algorithm is a
% duration dependant HMM, there is no need to calculate the A_matrix, as
% the transition between states is only dependant on the state durations.
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
% % Copyright (C) 2016  David Springer
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

function [B_matrix, pi_vector] = trainSchmidtSegmentationAlgorithm(PCGCellArray, annotationsArray, Fs, figures)


if(nargin < 4)
    figures = false;
end


%% Options

numberOfStates = 4;
numberOfPCGs = length(PCGCellArray);

% A matrix of the values from each state in each of the PCG recordings:
state_observation_values = cell(numberOfPCGs,numberOfStates);


for PCGi = 1:numberOfPCGs
    
    PCG_audio = PCGCellArray{PCGi};
    
    S1_locations = annotationsArray{PCGi,1};
    S2_locations = annotationsArray{PCGi,2};
    
    [PCG_Features, featuresFs] = getSchmidtPCGFeatures(PCG_audio, Fs);
    
    PCG_states = labelPCGStates(PCG_Features(:,1),S1_locations, S2_locations, featuresFs);
    
    
    %% Plotting assigned states:
    if(figures)
        figure('Name','Assigned states to PCG');
        
        t1 = (1:length(PCG_audio))./Fs;
        t2 = (1:length(PCG_Features))./featuresFs;
        
        plot(t1, PCG_audio, 'k-');
        hold on;
        plot(t2, PCG_Features, 'b-');
        plot(t2, PCG_states, 'r-');
        
        legend('Audio','Features','States');
        pause();
    end
    
    
    
    %% Group together all observations from the same state in the PCG recordings:
    for state_i = 1:numberOfStates
        state_observation_values{PCGi,state_i} = PCG_Features(PCG_states == state_i,:);
    end
end

% This line saves the "state_observation_values" variable in the main
% matlab workspace so that it can be investigated at a later time.
assignin('base', 'state_observation_values', state_observation_values)

%% Train the B and pi matrices after all the PCG recordings have been labelled:
[B_matrix, pi_vector] = trainBandPiMatricesSchmidt(state_observation_values);


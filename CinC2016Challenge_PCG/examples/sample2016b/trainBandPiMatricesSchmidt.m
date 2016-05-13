%function [B_matrix, pi_vector] = trainBandPiMatricesSchmidt(state_observation_values)
%
% Train the B matrix and pi vector for the HMM.
% The pi vector is the initial state probability, while the B matrix are
% the observation probabilities. In the case of Schmidt's algorith, the
% observation probabilities are based on a Gaussian distribution, trained
% on the labelled data:
%
%% Inputs:
% state_observation_values: an Nx4 cell array of observation values from
% each of N PCG signals for each (of 4) state. Within each cell is a KxJ
% double array, where K is the number of samples from that state in the PCG
% and J is the number of feature vectors extracted from the PCG.
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

function [B_matrix, pi_vector] = trainBandPiMatricesSchmidt(state_observation_values)

% Initialise the B_matrix as a 4x2 cell array. Each of the four states has
% two cell arrays - the first (B_matrix{state_i,1}) holds the mean value
% for the observations for that state. The second entry,
% (B_matrix{state_i,2}) holds the covariance matrix for the observations
% for each state.
B_matrix = cell(4,2);

%% Set pi_vector
% The true value of the pi vector, which are the initial state
% probabilities, are dependant on the heart rate of each PCG, and the
% individual sound duration for each patient. Therefore, instead of setting
% a patient-dependant pi_vector, simplify by setting all states as equally
% probable:
pi_vector = [0.25,0.25,0.25,0.25];

%% Derive B matrix mean and covariance values:

statei_values = cell(4,1);

for PCGi = 1: length(state_observation_values)
    statei_values{1} = vertcat(statei_values{1},state_observation_values{PCGi,1});
    statei_values{2} = vertcat(statei_values{2},state_observation_values{PCGi,2});
    statei_values{3} = vertcat(statei_values{3},state_observation_values{PCGi,3});
    statei_values{4} = vertcat(statei_values{4},state_observation_values{PCGi,4});
end



%% Assign mean and covariance values to B_matrix:
for state_i = 1:4
    B_matrix{state_i,1} = mean(statei_values{state_i});
    B_matrix{state_i,2} = cov(statei_values{state_i});
end



% function [delta psi qt] = viterbiDecodePCG(observation_sequence, pi_vector, b_matrix,heartrate, systolic_time, Fs)
%
% This function calculates the delta and psi matrices associated with the
% duration-dependant Viterbi decoding algorithm. This algorithm is outlined
% in:
% L. R. Rabiner, ?A tutorial on hidden Markov models and selected
% applications in speech recognition,? Proc. IEEE, vol. 77, no. 2, pp. 
% 257?286, Feb. 1989.
%
% This code is implemented as outlined in the paper:
% S. E. Schmidt et al., "Segmentation of heart sound recordings by a 
% duration-dependent hidden Markov model," Physiol. Meas., vol. 31,
% no. 4, pp. 513-29, Apr. 2010.
%
% Developed by David Springer for comparison purposes in the paper:
% D. Springer et al., "Logistic Regression-HSMM-based Heart Sound 
% Segmentation," IEEE Trans. Biomed. Eng., In Press, 2015.
%
%% INPUTS:
% observation_sequence: The sequence of extracted features
% pi_vector: the array of initial state probabilities, dervived from
% "trainSchmidtSegmentationAlgorithm".
% b_matrix: the observation probabilities, dervived from
% "trainSchmidtSegmentationAlgorithm".
% heartrate: the heart rate of the PCG, extracted using
% "getHeartRateSchmidt"
% systolic_time: the duration of systole, extracted using
% "getHeartRateSchmidt"
% Fs: the sampling frequency of the observation_sequence

%% Outputs:
% delta: the matrix of highest probability along a single path, at time
% t, which accounts for the first t observations and ends in state S_i
% psi: the matrix of states that maximised delta for each t and j
% qt: the optomised state sequence
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

function [delta, psi, qt] = viterbiDecodePCG(observation_sequence, pi_vector, b_matrix,heartrate, systolic_time, Fs)

%% Preliminary
schmidt_options = default_Schmidt_HSMM_options;

T = length(observation_sequence);
N = 4; % Number of states

% Setting the maximum duration of a single state. This is set to an entire
% heart cycle:
max_duration_D = round((1*(60/heartrate))*Fs);

% Initialising the variables that are needed to find the optimal state path along
% the observation sequence.
% delta_t(j), as defined on page 264 of Rabiner, is the best score (highest
% probability) along a single path, at time t, which accounts for the first
% t observations and ends in State s_j.
delta = ones(T,N)*-inf;
% The argument that maximises the transition between states (this is
% basically the previous state that had the highest transition probability
% to the current state) is tracked using the psi variable.
psi = zeros(T,N);

% An additional variable, that is not included on page 264 or Rabiner, is
% the state duration that maximises the delta variable. This is essential
% for the duration dependant HMM.
psi_duration =zeros(T,N);

%% Setting up observation probs
observation_probs = zeros(T,N);

% From the multivariate normal B-matrix, find the probability of the 
% features derived from each sample being in each state:
for state_n = 1:N
    observation_probs(:,state_n) = mvnpdf(observation_sequence,cell2mat(b_matrix(state_n,1)),cell2mat(b_matrix(state_n,2)));
end

%% Setting up state duration probabilities, using Gaussian distributions:
% Schmidt's paper makes use of Gaussian timing distributions for each state
% to model the expected duration of each state:
[d_distributions, max_S1, min_S1, max_S2, min_S2, max_systole, min_systole, max_diastole, min_diastole] = get_duration_distributions(heartrate,systolic_time);



% To speed up computation, compute the probability of each state being d
% samples in duration ahead of computation, and save these values in an
% matrix:
duration_probs = zeros(N,max_duration_D);

for state_j = 1:N
    for d = 1:max_duration_D
        if(state_j == 1)
            duration_probs(state_j,d) = mvnpdf(d,cell2mat(d_distributions(state_j,1)),cell2mat(d_distributions(state_j,2)));
            
            %TODO Justify minimum length
            if(d < min_S1 || d > max_S1)
                duration_probs(state_j,d)= realmin;
            end
            
            
        elseif(state_j==3)
            duration_probs(state_j,d) = mvnpdf(d,cell2mat(d_distributions(state_j,1)),cell2mat(d_distributions(state_j,2)));
            
            %TODO Justify minimum length
            if(d < min_S2 || d > max_S2)
                duration_probs(state_j,d)= realmin;
            end
            
            
        elseif(state_j==2)
            
            duration_probs(state_j,d) = mvnpdf(d,cell2mat(d_distributions(state_j,1)),cell2mat(d_distributions(state_j,2)));
            
            %TODO Justify minimum length
            if(d < min_systole|| d > max_systole)
                duration_probs(state_j,d)= realmin;
            end
            
            
        elseif (state_j==4)
            
            duration_probs(state_j,d) = mvnpdf(d,cell2mat(d_distributions(state_j,1)),cell2mat(d_distributions(state_j,2)));
            
            %TODO Justify minimum length
            if(d < min_diastole ||d > max_diastole)
                duration_probs(state_j,d)= realmin;
            end
        end
    end
    duration_sum(state_j) = sum(duration_probs(state_j,:));
end

%% Perform the actual Viterbi Recursion:

qt = zeros(1,length(delta));
%% Initialisation Step

% Equation 32a and 69a:

delta(1,:) = log(pi_vector) + log(observation_probs(1,:)); %first value is the probability of intially being in each state * probability of observation 1 coming from each state

%Equation 32b
psi(1,:) = -1;

% The state duration probabilities are now used.
%Change the a_matrix to have zeros along the diagonal, therefore, only
%relying on the duration probabilities and observation probabilities to
%influence change in states:
%This would only be valid in sequences where the transition between states
%follows a distinct order.
a_matrix = [0,1,0,0;0 0 1 0; 0 0 0 1;1 0 0 0];

%% Run the core Viterbi algorith

if(schmidt_options.use_mex)
        
    %% Run Mex code
    % Running this computation in C will speed up the result significantly.
    % Ensure you have run the mex viterbi_Schmidt.c code on the
    % native machine before running this.
    % For more information about creating mex files, see:
    % http://uk.mathworks.com/help/matlab/matlab_external/introducing-mex-files.html
    
    [delta, psi, psi_duration] = viterbi_Schmidt(N,T,a_matrix,max_duration_D,delta,observation_probs,duration_probs,psi);
    
else
    
        
    %% Recursion
    %For the first D steps, neeed to calculate each delta seperately:
    
    %Equations 33a and 33b and 69a, b, c etc:
    %again, ommitting the p(d), as state could have started before t = 1
    
    
    %For first samples of the signal, less than the max duration of a state:
    %As the state duration probabilities cannot be used yet, find each state
    %by the transition and observation probabilities only:
    
    
    
    %For the rest of the signal, where t > max_duration of a state, the state
    % duration probabilities can now be used, as we know that we are at least
    % a maximum duration into the signal. This loop differs from the one above,
    % as we now also search over all the possible durations we could be in each
    % state with variable d = 1:max_duration_D. Therefore, we now search over
    % an "analysis window" of time d, taking into account the probability of a
    % state lasting for time d, as well as seeing all the observations within
    % that window in one state.
    
    %Change the a_matrix to have zeros along the diagonal, therefore, only
    %relying on the duration probabilities and observation probabilities to
    %influence change in states:
    for t = 2:T
        
        for j = 1:N
            emission_probs = 0;
            for d = 1:max_duration_D
                
                
                if(t-d>0)
                    
                    
                    
                    %The start of the analysis window, which is the current time
                    %step, minus d, the time horizon we are currently looking back,
                    %plus 1. The analysis window can be seen to be starting one
                    %step back each time the variable d is increased.
                    start = t - d;
                    
                    
                    
                    %Find the max_delta and index of that from the previous step
                    %and the transition to the current step:
                    %This is the first half of the expression of equation 33a from
                    %Rabiner:
                    [max_delta, max_index] = max(delta(start,:)+log(a_matrix(:,j))');
                    

                    %Find the normalised probabilities of the observations at only
                    %the time point at the start of the time window:
                    probs = prod(observation_probs(start:t,j));
                    
                    %Keep a running total of the emmission probabilities as the
                    %start point of the time window is moved back one step at a
                    %time. This is the probability of seeing all the observations
                    %in the analysis window in state j:
                    
                    if(probs == 0 || isnan(probs))
                        probs =realmin;
                    end
                    
                    emission_probs = log(probs);
                    
                    %Find the total probability of transitioning from the last
                    %state to this one, with the observations and being in the same
                    %state for the analysis window. This is the duration-dependant
                    %variation of equation 33a from Rabiner:
                    delta_temp = max_delta + (emission_probs)+ log((duration_probs(j,d)./duration_sum(j)));
                                       
                    %Unlike equation 33a from Rabiner, the maximum delta could come
                    %from multiple d values, or from multiple size of the analysis
                    %window. Therefore, only keep the maximum delta value over the
                    %entire analysis window:
                    %If this probability is greater than the last greatest,
                    %update the delta matrix and the time duration variable:
                    if(delta_temp>delta(t,j))
                        delta(t,j) = delta_temp;
                        psi(t,j) = max_index;
                        
                        psi_duration(t,j) = d;
                    end
                    
                end
            end
        end
    end
end


%% Termination
%1) Find the last most probable state
%2) From the psi matrix, find the most likely preceding state
%3) Find the duration of the last state from the psi_duration matrix
%4) From the onset to the offset of this state, set to the most likely state
%5) Repeat steps 2 - 5 until reached the beginning of the signal


%The initial steps 1-4 are equation 34b in Rabiner. 1) finds P*, the most
%likely last state in the sequence, 2) finds the state that precedes the
%last most likely state, 3) finds the onset in time of the last state
%(included due to the duration-dependancy) and 4) sets the most likely last
%state to the q_t variable.

%1)
[val state] = max(delta(T,:),[],2);

%2)
offset = T;
preceding_state = psi(offset,state);

%3)
% state_duration = psi_duration(offset, state);
onset = offset - psi_duration(offset,state)+1;

%4)
qt(onset:offset) = state;


%The state is then updated to the preceding state, found above, which must
%end when the last most likely state started in the observation sequence:
state = preceding_state;

count = 0;
%While the onset of the state is larger than the maximum duration
%specified:
while(onset > 2)
    
    %2)
    offset = onset-1;
    %     offset_array(offset,1) = inf;
    preceding_state = psi(offset,state);
    %     offset_array(offset,2) = preceding_state;
    
    
    %3)
    %     state_duration = psi_duration(offset, state);
    onset = offset - psi_duration(offset,state);
    
    %4)
    %     offset_array(onset:offset,3) = state;
    
    if(onset<2)
        onset = 1;
    end
    qt(onset:offset) = state;
    state = preceding_state;
    count = count +1;
    
    if(count> 10000)
        break;
    end
end



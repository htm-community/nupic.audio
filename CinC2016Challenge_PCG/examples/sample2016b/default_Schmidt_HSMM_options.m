% function schmidt_options = default_Schmidt_HSMM_options()
%
% The default options to be used with the Schmidt segmentation algorithm.
% USAGE: schmidt_options = default_Schmidt_HSMM_options
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


function schmidt_options = default_Schmidt_HSMM_options()


%% The sampling frequency at which to extract signal features:
schmidt_options.audio_Fs = 1000;

%% The downsampled frequency
%Set to 50 in Schmidt paper
schmidt_options.audio_segmentation_Fs = 50;


%% Tolerance for S1 and S2 localization
schmidt_options.segmentation_tolerance = 0.1;%seconds

%% Whether to use the mex code or not:
schmidt_options.use_mex = true;


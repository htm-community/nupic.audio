function classifyResult = classifyFromHsIntervals(features)
%
% This function gives the classification result for heart sound recording
% using the obtained features
%
%
% INPUTS:
% features: the obtained features
%
% OUTPUTS:
% classifyResult: classification result for the heart sound recording
% classifyResult = 1 for abnormal recording
%                = -1 for normal recording
%                = 0 for unsure recording (too noisy)
%
%
% Written by: Chengyu Liu, January 22 2016
%             chengyu.liu@emory.edu
%
% Last modified by:
%
%
% $$$$$$ IMPORTANT
% Please note: the following classificaiton rule (formula) was based on the feature
% selection results using the logistic regression model from the 20 features on the balanced training database.
% You can construct the more accurate classification rule based on the obtained featuers, or
% based on the features you generated, or other information you think useful


%% Feature selection results when performing logistic regression on balanced training database 
weight            = [-2.7	0.079	0.047	0.060]; % feature weights, the first weight is the constant value
% weight            = [-2.918	-0.031	0.077	0.053	0.025	-0.011	-0.005]; % feature weights, the first weight is the constant value
features_selected = [features(4),features(8),features(20)];  % selected featuers usingthe logistic regression model

%% Calculation the output using the prediction formula
thr  = 0; % classification threshold, thr>0 for abnormal recordings.
pred = weight(1);
for i = 1:length(weight)-1
    pred = pred + weight(i+1)*features_selected(i);
end

%% Calssificaiton
% we only provide the normal/abnormal classification, if you think the
% current recording is too noisy, you can set classifyResult=0. The score
% function will consider the classifyResult=0 situations.
if pred > thr
    classifyResult = 1;
else
    classifyResult = -1;
end


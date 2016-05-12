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

%% You can use the logistic regression model to train the classification model to obtian the predictor for normal/abnormal classification
% Reference codes for using logistic regression model are given as follows:

% [B,dev,stats] = glmfit(features, Reference_labels, 'binomial','link','logit');  
% % features: the obtained features; 
% % Reference_labels: reference classification results, for glmfit.m,Reference_labels should be binary inputs (1 for abnormal and 0 for normal)
% predictor     = glmval(B,features,'logit',stats);
% % the typical thr=0.5 is used for calssifying abnormal (predictor>=thr) and normal (predictor<thr)

%% We give the B metrix by training logistic regression model on the validation set to facilitate your use 
% % You are strongly suggested to re-train the logistic regression model on all training set to update the B metrix to obtain more accurate classification results. 

B = [-4.55969671153671;-0.0190844674392002;-0.00365674916123946;0.0464309139962342;0.0382411423829992;-0.0144478229473877;0.0169187704188220;0.0182152301056541;0.0166856367355031;0.0242221034823620;-0.0124936707725577;0.121391485490513;0.228393275829136;-0.0379380232270407;0.407767267634115;-0.0335230435994371;0.0834749593084066;-0.0118791358148168;0.0191288105549299;0.00948554070687907;0.0502122854641683];
predictor = glmval(B,features,'logit');

%% Calssificaiton
% we only provide the normal/abnormal classification, if you think the
% current recording is too noisy, you can set classifyResult=0. The score
% function will consider the classifyResult=0 situations.
thr  = 0.5; % classification threshold, thr>0.5 for abnormal recordings.
if predictor > thr
    classifyResult = 1;
else
    classifyResult = -1;
end


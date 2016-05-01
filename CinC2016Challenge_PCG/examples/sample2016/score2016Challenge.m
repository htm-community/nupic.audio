% This script will score your algorithm for classification accuracy, based on the reference classification results.
% Your final score for the challenge will be evaluated on the hidden test set.
%
% This script requires that you first run generateValidationSet.m
%
%
% Written by: Chengyu Liu, Fubruary 15 2016
%             chengyu.liu@emory.edu
%
% Last modified by:
%
%

clear all;

w_unsure = 0.5;  % count weight for true positive and true negative recording classification if a sound recording scored as 0 (unsure/too noisy)

%% Load the answer classification results
fid = fopen('answers.txt','r');
if(fid ~= -1)
    ANSWERS = textscan(fid, '%s %d', 'Delimiter', ',');
else
    error('Could not open users answer.txt for scoring. Run the generateValidationSet.m script and try again.')
end
fclose(fid);

%% Load the reference classification results
reffile = ['validation' filesep 'REFERENCE.csv'];
fid = fopen(reffile, 'r');
if(fid ~= -1)
    Ref = textscan(fid,'%s %d','Delimiter',',');
else
    error(['Could not open ' reffile ' for scoring. Exiting...'])
end
fclose(fid);

RECORDS = Ref{1};
target  = Ref{2};
N       = length(RECORDS);

a = find(ANSWERS{2}==0);
b = find(ANSWERS{2}==1);
c = find(ANSWERS{2}==-1);
ln = length(a)+length(b)+length(c);
if(length(ANSWERS{2}) ~= ln);
    error('Input must contain only -1, 1 or 0');
end

%% Scoring
% We do not assume that the references and the answers are sorted in the
% same order, so we search for the location of the individual records in answer.txt file.
TP=0;
FN=0;
FP=0;
TN=0;

for n = 1:N
    rec = RECORDS{n};
    i = strmatch(rec, ANSWERS{1});
    if(isempty(i))
        warning(['Could not find answer for record ' rec '; treating it as unknown.']);
        this_answer = 0;
    else
        this_answer = ANSWERS{2}(i);
    end
    if target(n)==1
        if this_answer==1
            TP = TP+1;
        elseif this_answer==-1
            FN = FN+1;
        else
            TP = TP+w_unsure;
            FN = FN+1-w_unsure;
        end
    else
        if this_answer==1
            FP = FP+1;
        elseif this_answer==-1
            TN = TN+1;
        else
            TN = TN+w_unsure;
            FP = FP+1-w_unsure;
        end
    end
end

Se   = TP/(TP+FN); % Sensibility
Sp   = TN/(TN+FP); % Specificity
MAcc = (Se+Sp)/2;  % Modified accuracy measure

str = ['  Sensibility:  ' '%1.4f\n'];
fprintf(str,Se)
str = ['  Specificity:  ' '%1.4f\n'];
fprintf(str,Sp)
str = ['  Final modified accuracy (MAcc):  ' '%1.4f\n'];
fprintf(str,MAcc)




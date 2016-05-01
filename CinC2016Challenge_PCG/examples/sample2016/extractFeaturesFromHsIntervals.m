function features = extractFeaturesFromHsIntervals(assigned_states, PCG)
%
% This function calculate 20 features based on the assigned_states by running "runSpringerSegmentationAlgorithm.m" function
%
% INPUTS:
% assigned_states: the array of state values assigned to the sound recording.
% PCG: resampled sound recording with 1000 Hz.
%
% OUTPUTS:
% features: the obtained 20 features for the current sound recording
%
%
% Written by: Chengyu Liu, January 22 2016
%             chengyu.liu@emory.edu
%
% Last modified by:
%
%
% $$$$$$ IMPORTANT
% Please note: the calculated 20 features are only some pilot features, some features maybe
% helpful for classifying normal/abnormal heart sounds, some maybe
% not. You need re-construct the features for a more accurate classification.


%% We just assume that the assigned_states cover at least 2 whole heart beat cycle
indx = find(abs(diff(assigned_states))>0); % find the locations with changed states

if assigned_states(1)>0   % for some recordings, there are state zeros at the beginning of assigned_states
    switch assigned_states(1)
        case 4
            K=1;
        case 3
            K=2;
        case 2
            K=3;
        case 1
            K=4;
    end
else
    switch assigned_states(indx(1)+1)
        case 4
            K=1;
        case 3
            K=2;
        case 2
            K=3;
        case 1
            K=0;
    end
    K=K+1;
end

indx2                = indx(K:end);
rem                  = mod(length(indx2),4);
indx2(end-rem+1:end) = [];
A                    = reshape(indx2,4,length(indx2)/4)'; % A is N*4 matrix, the 4 columns save the beginnings of S1, systole, S2 and diastole in the same heart cycle respectively

%% Feature calculation
m_RR        = round(mean(diff(A(:,1))));             % mean value of RR intervals
sd_RR       = round(std(diff(A(:,1))));              % standard deviation (SD) value of RR intervals
mean_IntS1  = round(mean(A(:,2)-A(:,1)));            % mean value of S1 intervals
sd_IntS1    = round(std(A(:,2)-A(:,1)));             % SD value of S1 intervals
mean_IntS2  = round(mean(A(:,4)-A(:,3)));            % mean value of S2 intervals
sd_IntS2    = round(std(A(:,4)-A(:,3)));             % SD value of S2 intervals
mean_IntSys = round(mean(A(:,3)-A(:,2)));            % mean value of systole intervals
sd_IntSys   = round(std(A(:,3)-A(:,2)));             % SD value of systole intervals
mean_IntDia = round(mean(A(2:end,1)-A(1:end-1,4)));  % mean value of diastole intervals
sd_IntDia   = round(std(A(2:end,1)-A(1:end-1,4)));   % SD value of diastole intervals

for i=1:size(A,1)-1
    R_SysRR(i)  = (A(i,3)-A(i,2))/(A(i+1,1)-A(i,1))*100;
    R_DiaRR(i)  = (A(i+1,1)-A(i,4))/(A(i+1,1)-A(i,1))*100;
    R_SysDia(i) = R_SysRR(i)/R_DiaRR(i)*100;
    
    P_S1(i)     = sum(abs(PCG(A(i,1):A(i,2))))/(A(i,2)-A(i,1));
    P_Sys(i)    = sum(abs(PCG(A(i,2):A(i,3))))/(A(i,3)-A(i,2));
    P_S2(i)     = sum(abs(PCG(A(i,3):A(i,4))))/(A(i,4)-A(i,3));
    P_Dia(i)    = sum(abs(PCG(A(i,4):A(i+1,1))))/(A(i+1,1)-A(i,4));
    if P_S1(i)>0
        P_SysS1(i) = P_Sys(i)/P_S1(i)*100;
    else
        P_SysS1(i) = 0;
    end
    if P_S2(i)>0
        P_DiaS2(i) = P_Dia(i)/P_S2(i)*100;
    else
        P_DiaS2(i) = 0;
    end
end

m_Ratio_SysRR   = mean(R_SysRR);  % mean value of the interval ratios between systole and RR in each heart beat
sd_Ratio_SysRR  = std(R_SysRR);   % SD value of the interval ratios between systole and RR in each heart beat
m_Ratio_DiaRR   = mean(R_DiaRR);  % mean value of the interval ratios between diastole and RR in each heart beat
sd_Ratio_DiaRR  = std(R_DiaRR);   % SD value of the interval ratios between diastole and RR in each heart beat
m_Ratio_SysDia  = mean(R_SysDia); % mean value of the interval ratios between systole and diastole in each heart beat
sd_Ratio_SysDia = std(R_SysDia);  % SD value of the interval ratios between systole and diastole in each heart beat

indx_sys = find(P_SysS1>0 & P_SysS1<100);   % avoid the flat line signal
if length(indx_sys)>1
    m_Amp_SysS1  = mean(P_SysS1(indx_sys)); % mean value of the mean absolute amplitude ratios between systole period and S1 period in each heart beat
    sd_Amp_SysS1 = std(P_SysS1(indx_sys));  % SD value of the mean absolute amplitude ratios between systole period and S1 period in each heart beat
else
    m_Amp_SysS1  = 0;
    sd_Amp_SysS1 = 0;
end
indx_dia = find(P_DiaS2>0 & P_DiaS2<100);
if length(indx_dia)>1
    m_Amp_DiaS2  = mean(P_DiaS2(indx_dia)); % mean value of the mean absolute amplitude ratios between diastole period and S2 period in each heart beat
    sd_Amp_DiaS2 = std(P_DiaS2(indx_dia));  % SD value of the mean absolute amplitude ratios between diastole period and S2 period in each heart beat
else
    m_Amp_DiaS2  = 0;
    sd_Amp_DiaS2 = 0;
end

features = [m_RR sd_RR  mean_IntS1 sd_IntS1  mean_IntS2 sd_IntS2  mean_IntSys sd_IntSys  mean_IntDia sd_IntDia m_Ratio_SysRR sd_Ratio_SysRR m_Ratio_DiaRR sd_Ratio_DiaRR m_Ratio_SysDia sd_Ratio_SysDia m_Amp_SysS1 sd_Amp_SysS1 m_Amp_DiaS2 sd_Amp_DiaS2];





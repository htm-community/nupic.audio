function irn = makeIRNo(Delay,NIt,Dur,Gate,RMS,TS,DelF1,HPF,LPF,DelF2)
% irn = makeIRNo(Delay,NIt,Dur,Gate,RMS,TS,DelF1,HPF,LPF,DelF2)
% 
%   Delay = IRN delay in ms;
%   NIt = number of iterations;
%   Dur = duration of IRN;
%   Gate = duration of on- and offset ramps;
%   RMS = RMS amplitude of IRN;
%   TS = sampling period in ms;
%   Delf1 = lower spectral ramp (we used 0.2 kHz);
%   HPF = lower edge of stady-state portion 
%       (in the experiment, HPF was 0.8, 1.6, 3.2 or 6.4 kHz);
%   LPF = upper edge of steady-state portion 
%       (in the experiment, LPF was always 1.6 kHz above HPF);
%   DelF2 = upper lower spectral ramp (we used 1.6 kHz);
%
% irn = makeIRNo(16,8,100,10,.1,.05,.2,.5,2.0,1.6)

TPts = round(Dur/TS);
FPts = lcfFPts(TPts);
cmbFilter = lcfFilter(Delay,NIt,TPts,FPts,TS,DelF1,HPF,LPF,DelF2);
array = real(ifft(cmbFilter.*fft(randn(1,FPts))));
irn = lcfQWind(lcfSetI(array(1:TPts),RMS),Gate,TS);
irn = lcfSetI(irn,RMS);
wavwrite(irn,1000/TS,'testwave');

% ********** lcfFilter **********
function cmbFilter = lcfFilter(Delay,NIt,TPts,FPts,TS,DelF1,HPF,LPF,DelF2)

DF = 1/(TS*FPts);
SDelF1 = round(DelF1/DF);
SDelF2 = round(DelF2/DF);
SBW = round((LPF-HPF)/DF);
FL = max(HPF-DelF1,0); 
FH = min(LPF+DelF2,1/(2*TS)); 

bpFilter = zeros(1,round(FL/DF));
LEN = min(SDelF1,round(HPF/DF)-length(bpFilter));
jwd = fliplr(cos((0:LEN-1)*pi/(2*SDelF1)));
bpFilter = [bpFilter jwd]; 
bpFilter = [bpFilter ones(1,SBW)];

LEN = min(min(FPts/2,round(FH/DF))-length(bpFilter),SDelF2);
jwd = cos((0:(LEN-1))*pi/(2*SDelF2));
bpFilter = [bpFilter jwd];
bpFilter = [bpFilter zeros(1,FPts/2-length(bpFilter))];

frq = (0:FPts/2-1)*DF;
%Erb = sum(bpFilter.^2*DF);

G = 1;
reH = ones(1,FPts/2);
imH = zeros(1,FPts/2);
for I = 1:NIt 
    reH = reH+G^I*cos(2*pi*I*Delay*frq);
    imH = imH+G^I*sin(2*pi*I*Delay*frq);
end
cmbFilter = bpFilter.*(reH+i*imH);   
cmbFilter = [cmbFilter fliplr(cmbFilter)];

% ************ lcfFPts ***********
function FPts = lcfFPts(TPts)

FPts = 16384;
while FPts<TPts
   FPts = FPts*2;
end

% ************ lcfSetI ************
function out = lcfSetI(in,RMS);

S = sqrt(mean(in.^2));
if S>0
    out = in*RMS/S;
else
    error('==> RMS: Devide by zero!')
end

% ************ lcfQWind ************
function out = lcfQWind(in,Gate,TS)

GPts = round(Gate/TS);
APts = length(in);
if APts<2*GPts
    error('==> ''Dur'' must be longer than two times ''Gate''!') 
end
env = cos(pi*(0:GPts-1)/(2*(GPts-1))).^2;
out = [1-env ones(1,APts-2*GPts) env].*in;


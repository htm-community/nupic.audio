

function [spokes, target] = get_spoke_points(target_pitch,target_scale,...
                                            pitch_radius,scale_radius,...
                                            spoke_grad,no_spokes,...
                                            no_per_spoke)

if ~exist('target_pitch')
    fprintf('Using default parameters for get_spoke_points\n');
    % default values for get_spoke_points
    target_pitch = 171.7;
    target_scale = 165/146.9*100;%105.8;
    pitch_radius = 4; % in semitones
    scale_radius = 6; % in pseudo semitones
    spoke_grad   = 0.22; % gradient of first spoke, closest to origin
    no_spokes    = 8;
    no_per_spoke = 7;
end
target = [target_pitch, target_scale];

% calculate max values on ellipse for each coordinate
pitch_max   = target_pitch * 2^(pitch_radius/12);
scale_max   = target_scale * 2^(scale_radius/12);

% convert all values into log domain
target_p_log    = log(target_pitch);
target_s_log    = log(target_scale);
max_p_log       = log(pitch_max);
max_s_log       = log(scale_max);

% using parametric equations for ellipse
a = max_p_log - target_p_log; % semi-axis in pitch direction
b = max_s_log - target_s_log; % semi_axis in scale direction

t = atan(spoke_grad) + pi;

alpha = (0:no_spokes-1) * 2*pi/(no_spokes) + t;

pitch_log = a*cos(alpha) + target_p_log;
scale_log = b*sin(alpha) + target_s_log;

spokes = cell(no_spokes,1);

for i = 1:no_spokes
    
    vector      = [target_p_log-pitch_log(i), target_s_log-scale_log(i)];
    numerator   = ([0:no_per_spoke]).^2;
    
    
    
    for j = 1:no_per_spoke
        
        coords(no_per_spoke+1-j,1:2) = [pitch_log(i),scale_log(i)] + vector*(numerator(no_per_spoke+1)-numerator(j+1))/numerator(no_per_spoke+1);
        
    end
    
    spokes{i} = exp(coords);
%     spokes{i} = coords;
    
end


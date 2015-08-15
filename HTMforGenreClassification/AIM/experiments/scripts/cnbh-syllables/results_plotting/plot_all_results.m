% Plot a figure based on recognition data from the HTK-AIM features
% experiments - a reworking of the 'spider plots' by Jess Monaghan, 
% Nick Fyson and Martin Vestergaard.
% Copyright 2009 University of Cambridge
% Author: Tom Walters <tcw24@cam>
function plot_all_results(exp_path, iteration, plot_end_numbers)

plot_numbers = true;
if nargin < 3
  plot_end_numbers = false;
end

% Load the results from the experimental directory
misclassified = load([exp_path 'misclassified_syllables_iteration_' num2str(iteration)]); 

% The total number of syllables in the CNBH syllable database 
num_points = 185;
target_VTL = 15;

misclassified(:, 1) = 1 - misclassified(:, 1) / num_points;

% The individual data points are plotted as spheres
sphere_size_x = 1.2;
sphere_size_y = 0.17;
sphere_size_z = 2.5;

% Get the location of the various points on the spoke pattern
[spokes, target] = get_spoke_points();
results = {};

% Fill the results vector
for i = 1:length(spokes)
  results{i} = zeros(length(spokes{1}),1);
  r=round(spokes{i}*10)/10;
  for j = 1:length(spokes{i})
      result =  misclassified(misclassified(:,3) == r(j,2) ...
                                    & misclassified(:,2) == r(j,1), 1);
      if result
        results{i}(j) = result;
      else
        results{i}(j) = 1.0;
      end
  end
  results{i} = 100.0 * results{i};
  spokes{i}(:,2) = target_VTL * target(2) ./ spokes{i}(:,2);
end

figure1 = figure;
axes1 = axes('Parent',figure1,'YScale','log','YMinorTick','on',...
    'YMinorGrid','on',...
    'XScale','log',...
    'XMinorTick','on',...
    'XMinorGrid','on');

shades = 50;
cmap = fliplr(autumn(shades));
for i=1:length(spokes)
  
  hold on;
  j=1;
  x_pos = spokes{i}(j, 1);
  y_pos = spokes{i}(j, 2);
  z_pos = results{i}(j);
  j=2;
  x_pos_2 = spokes{i}(j, 1);
  y_pos_2 = spokes{i}(j, 2);
  z_pos_2 = results{i}(j);
  
  j=1;
  
  if (~plot_numbers && plot_end_numbers)
    text(x_pos + 0.3*(x_pos - x_pos_2), y_pos + 0.3*(y_pos - y_pos_2), z_pos + 0.3*(z_pos - z_pos_2) , [num2str(results{i}(j), 3) '%']);
  end
  for j = 1:length(spokes{i})
	if (plot_numbers)
	  text(spokes{i}(j,1), spokes{i}(j,2), results{i}(j), [num2str(results{i}(j), 3) '%']);
	else
      [X Y Z] = sphere(10);
      X = sphere_size_x.*X + spokes{i}(j,1);
      Y = sphere_size_y.*Y + spokes{i}(j,2);
      Z = sphere_size_z.*Z + results{i}(j);
      % C = zeros(size(X));
      plot3([spokes{i}(j, 1) spokes{i}(j, 1)], ...
            [spokes{i}(j, 2),spokes{i}(j, 2)], [0 results{i}(j)], '-k.', ...
            'LineWidth', 1, 'Color', [0.8 0.8 0.8]);
      surf(X, Y, Z, ones(size(Z)) .* (results{i}(j)), 'LineStyle', 'none');
    end
  end
  if (~plot_numbers)
    plot3(spokes{i}(:,1), spokes{i}(:,2), results{i}(:), '-', 'LineWidth', 2, ...
         'Color', [0.2 0.2 0.2]);
  end
end
% Plot a zero-sized sphere at zero to get the autoscaling of the colour bar
% correct
[X Y Z] = sphere(20);
X = zeros(size(X)) - 1;
surf(X, X, X, ones(size(Z)) .* 0, 'LineStyle', 'none');
%colorbar('WestOutside');
view([-80 60]);
grid('on');
xlim([132 224]);
zlim([0 100]);
ylim([10 22]);
set(gca, 'FontSize', 12);
%set(gca, 'FontName', 'Hoefler Text');
xlabel('GPR /Hz');
ylabel('VTL /cm');
zlabel('Percent correct');
set(axes1, 'YScale', 'log');
set(axes1, 'XScale', 'log');
set(axes1, 'XTick', [132 172 224]);
set(axes1, 'YTick', [10 15 22]);
set(axes1, 'YDir', 'reverse');
set(axes1, 'ZTick', [0 20 40 60 80 100]);
hold('all');
%print('-depsc', [exp_path 'results_plot_iteration_' num2str(iteration) '.eps']);
%   saveas(gcf, [exp_path 'results_plot_iteration_' num2str(iteration) '.fig']);
%!open results_plot.eps




work_paths = {'nap_2/', 'mfcc/'};
%colors = jet(length(work_paths));
colors=[0 0 0; 1 0 0];
figure;

for type=1:length(work_paths)
  work_path = work_paths{type};
  %work_path = 'mfcc/';
  nap_results = load([work_path 'final_results.txt']);

  states_set = min(nap_results(:,1))+1:2:max(nap_results(:,1));
  mix_set = min(nap_results(:,2))+1:2:max(nap_results(:,2));
  total_lines = length(states_set) * length(mix_set);


  line_names = cell(total_lines,1);
  line_styles = {'-', '--', ':', '-.'};
  marker_styles = {'+','o','*','.','x','s','d','^'};

  %colors = jet(length(mix_set));
  
  val = 1;
  for states = states_set
    line_style = line_styles{1 + mod(states, length(states_set))};
    
    for components = mix_set
      marker_style = marker_styles{1 + mod(components, length(mix_set))};
      line_names{val,1} = [num2str(states) ' states ' num2str(components) ' components'];
      nr = nap_results(nap_results(:,1) == states, :);
      nr = nr(nr(:,2) == components, :);
      nr = sortrows(nr,3);
      plot(nr(:,3), nr(:,4), 'Color', colors(type, :), 'Linewidth', 1, 'LineStyle', line_style, 'Marker', marker_style);
      hold on;
      val = val + 1;
    end
  end
  
  xlabel('Training Iterations');
  ylabel('Percent Correct');
  ylim([50 100]);
  %ylim([86.9 93.3]);
  xlim([4.5 15.5]);
  set(gca, 'XTick', 5:15);
end
legend(line_names, 'Location', 'EastOutside');
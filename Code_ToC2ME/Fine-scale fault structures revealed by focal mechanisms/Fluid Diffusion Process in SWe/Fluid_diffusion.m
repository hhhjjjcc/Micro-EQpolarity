clear;
clc;
% Read the data file, ensuring that event_time is read as a string
file_path = 'mt_solution_20250319_SKHASH_SWe_quality_A_B_without_northest_low_dip.txt';
opts = detectImportOptions(file_path, 'Delimiter', '\t', 'ReadVariableNames', false);
opts.VariableTypes{1} = 'string';  % Force event_time_str to be read as a string
data = readtable(file_path, opts);

% Extract data columns
event_time_str = data.Var1;   % Time string column
evla_sw = data.Var2;          % Latitude column
evlo_sw = data.Var3;          % Longitude column
depth_sw = data.Var4;         % Depth column
strike_sw = data.Var5;        % Strike column
dip_sw = data.Var6;           % Dip column
rake_sw = data.Var7;          % Rake column
flag_sw = data.Var8;          % Flag column

% Convert time string to datetime format
evtime_sw = NaT(size(event_time_str)); % Initialize datetime array
for i = 1:length(event_time_str)
    year = str2double(event_time_str{i}(1:4));
    month = str2double(event_time_str{i}(5:6));
    day   = str2double(event_time_str{i}(7:8));
    hour  = str2double(event_time_str{i}(9:10));
    minute= str2double(event_time_str{i}(11:12));
    second= str2double(event_time_str{i}(13:end));
    
    evtime_sw(i) = datetime(year, month, day, hour, minute, second);
end

% Latitude and Longitude -> Plane coordinates
[evlo_m, evla_m] = latlon2xy(evlo_sw, evla_sw, min(evlo_sw), min(evla_sw));

%% Figure 1: Projection scatter plot
figure('pos', [1500, 800, 500, 600]);
scatter(evlo_m, evla_m, 30, 'filled');  
colormap(parula); 
hold on;
ylabel('Northing (m)', 'FontSize', 16);
xlabel('Easting (m)', 'FontSize', 16);
axis tight;
grid on;
set(gca, 'FontSize', 16);

% Find the first time point corresponding to the longitude and latitude and convert to projection coordinates
[evtime_o, ind_o] = min(evtime_sw);
evla_o = evla_sw(ind_o);
evlo_o = evlo_sw(ind_o);
[evlo_first, evla_first] = latlon2xy(evlo_o, evla_o, min(evlo_sw), min(evla_sw));
scatter(evlo_first, evla_first, 30, 'filled');  % First point

saveas(gcf, 'evlo_evla_scatter.png');

%% Calculate the time difference (hours) and distance (meters) for each event relative to the first event
T = zeros(length(evlo_m), 1);
D = zeros(length(evlo_m), 1);
for i = 1:length(evlo_m)
    T(i) = hours(evtime_sw(i) - evtime_o);
    
    dla = evla_sw(i) - evla_o;
    dist_m = deg2km(distance(evla_sw(i), evlo_sw(i), evla_o, evlo_o)) * 1000;
    % If the latitude difference is negative, take the negative distance
    D(i) = (dla >= 0) * dist_m + (dla < 0) * (-dist_m);
end

%% Figure 2: Observed data + diffusion simulation curves
time = 0:0.1:35;       % Days 0-35 with interval 0.1 days
time = time * 24;      % Convert to hours

% Migration rate (m^2/s), note that it is in ascending order: 0.01, 0.0316, 0.1
rate = 10.^([-2:0.5:-1])';  
% Calculate positive and negative diffusion distances
difs  = sqrt(rate * time * 4 * pi * 3600);  % Positive diffusion (meters)
difs2 = -difs;                              % Negative diffusion

figure('pos', [1200, 800, 600, 600]); 
hold on; grid on;

% Plot observed data scatter (use fixed color to avoid conflicts with lines)
hData = scatter(T, D, 30, 'MarkerFaceColor', '#005A9C', 'MarkerEdgeColor', '#005A9C', ...
    'DisplayName', 'Observed Data');

% Get color map
colors = lines(length(rate));

% Plot each diffusion curve
for i = 1:length(rate)
    % Positive diffusion curve
    if i == length(rate)-1  % Assume the last line is the best fit
        hLine = plot(time, difs(i,:), '--', 'LineWidth', 1.5, 'Color', colors(i,:), ...
            'DisplayName', sprintf('Rate = %.3g m^2/s (Best Fit)', rate(i)));
    else
        hLine = plot(time, difs(i,:), '--', 'LineWidth', 1.5, 'Color', colors(i,:), ...
            'DisplayName', sprintf('Rate = %.3g m^2/s', rate(i)));
    end
    
    % Negative diffusion curve (not included in the legend)
    plot(time, difs2(i,:), '--', 'LineWidth', 1.5, 'Color', colors(i,:), ...
        'HandleVisibility','off');
end

xlabel('Time (hours)', 'FontSize', 16);
ylabel('Distance (m)', 'FontSize', 16);

% Automatically read all handles with DisplayName and generate legend
legend('show', 'Location', 'northeast', 'FontSize', 12);

xlim([0 250]);
set(gca, 'FontSize', 16);

saveas(gcf, 'diffusion_plot.png');

%% Latitude and Longitude to plane coordinates function
function [x, y] = latlon2xy(lon, lat, lonmin, latmin)
    dconst = 6378.0 * pi / 180.0;
    x = zeros(size(lon));
    y = zeros(size(lat));
    for i = 1:length(lon)
        y(i) = (lat(i) - latmin) * dconst;
        x(i) = (lon(i) - lonmin) * cos(lat(i) / 180 * pi) * dconst;
    end
end

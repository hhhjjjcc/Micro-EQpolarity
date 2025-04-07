import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import locale

# Set locale to English for consistent date formatting
locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')

# File paths
original_file_path = './mt_solution_20241114_SKHASH_quality_A_West_Fault_with_mag.txt'
fracture_file_path = './StageTimeLocation_ToC2ME_2.txt'
injection_volume_file_path = './injection_volume.csv'

# Original data column names
original_column_names = ['evid', 'evla', 'evlo', 'depth', 'strike', 'dip', 'rake', 'misfit', 'magnitude']
fracture_column_names = ['year', 'month', 'day', 'hour', 'longitude', 'latitude', 'unknown']

# Define the data ranges for each well
well_ranges = {
    'WellA': (1, 21),
    'WellB': (22, 45),
    'WellC': (46, 170),
    'WellD': (171, 186)
}

# Define colors for each well
well_colors = {
    'WellA': 'green',
    'WellB': 'blue',
    'WellC': 'purple',
    'WellD': 'red'
}

# Read original data
original_data = pd.read_csv(original_file_path, sep='\t', header=None, names=original_column_names, dtype={'evid': str})

# Parse evid to timestamp
def parse_evid_to_time(evid):
    year = int(evid[0:4])
    month = int(evid[4:6])
    day = int(evid[6:8])
    hour = int(evid[8:10])
    minute = int(evid[10:12])
    second = int(evid[12:14])
    millisecond = int(float('0' + evid[14:]) * 1000)
    return datetime(year, month, day, hour, minute, second, millisecond * 1000)

original_data['time'] = original_data['evid'].apply(parse_evid_to_time)

# Process strike data
def process_strike(strike):
    if strike > 270:
        return strike - 180
    elif strike < 90:
        return strike + 180
    else:
        return strike

original_data['processed_strike'] = original_data['strike'].apply(process_strike)
original_data = original_data.sort_values(by='time')

# Read fracture data
fracture_data = pd.read_csv(fracture_file_path, sep=' ', header=None, names=fracture_column_names)

# Handle missing values and force conversion to integers
fracture_data[['year', 'month', 'day', 'hour']] = fracture_data[['year', 'month', 'day', 'hour']].fillna(0).astype(int)

# Parse time
def parse_time(row):
    return datetime(int(row['year']), int(row['month']), int(row['day']), int(row['hour']))

fracture_data['time'] = fracture_data.apply(parse_time, axis=1)

# Keep only the earliest vertical line for each well
fracture_data['well'] = ''
for well, (start, end) in well_ranges.items():
    well_data = fracture_data.iloc[start-1:end]  
    earliest_time = well_data['time'].min()
    fracture_data.loc[fracture_data['time'] == earliest_time, 'well'] = well

fracture_data = fracture_data[fracture_data['well'] != '']

# Read injection volume data
injection_data = pd.read_csv(injection_volume_file_path)
injection_data['Date'] = pd.to_datetime(injection_data['Date'])

def classify_groups(strike, dip, rake):
    if ((0 <= strike <= 12) or (170 <= strike <= 192) or (355 <= strike <= 360)) and ((165 <= rake <= 180) or (-180 <= rake <= -165)): # from 0/180: 8 degree
        return 'group1'
    elif ((19 <= strike <= 60) or (200 <= strike <= 231)) and ((165 <= rake <= 180) or (-180 <= rake <= -165)): # from 0/180: 19-35 degree
        return 'group2'
    elif ((185 <= strike <= 200) and (43 <= dip <= 65)) and ((165 <= rake <= 180) or (-180 <= rake <= -165)): # group3
        return 'group3'
    elif ((12 <= strike < 19) or (192 <= strike <= 200) or (185 <= strike <= 195)) and ((165 <= rake <= 180) or (-180 <= rake <= -165)): # from 0/180: 12-19 degree
        return 'group4'
    else:
        return 'group_other'

# Apply the classification function and get corresponding colors
group_colors = {
    'group1': (1, 0, 0),      # Red
    'group2': (0, 0.8, 1),    # Light blue
    'group3': (0, 0.8, 0),    # Green
    'group4': (1, 0.7, 0),    # Orange
    'group_other': (1, 0.84, 0)  # Gold
}
original_data['group'] = original_data.apply(lambda row: classify_groups(row['strike'], row['dip'], row['rake']), axis=1)

# Plotting
fig, ax1 = plt.subplots(figsize=(10, 6))

# Left axis: Plot the earthquake event scatter plot
scatter_sizes = (original_data['magnitude'] + 4) ** 3
used_groups = []  # Keep track of the used groups for the legend
for group, color in group_colors.items():
    group_data = original_data[original_data['group'] == group]
    if not group_data.empty:  # Check if group has data
        ax1.scatter(group_data['time'], group_data['processed_strike'], 
                    color=color, alpha=0.6, edgecolors='w', 
                    s=scatter_sizes[group_data.index], label=group)
        used_groups.append(group)

# Plot the vertical lines, only the earliest vertical line for each well
for well, color in well_colors.items():
    well_data = fracture_data[fracture_data['well'] == well]
    for _, row in well_data.iterrows():
        ax1.axvline(row['time'], color=color, alpha=0.6, label=well if well not in ax1.get_legend_handles_labels()[1] else "")

ax1.set_ylabel('Strike', fontsize=13)  # Adjust y-axis label font size
ax1.set_xlabel('Time', fontsize=13)   # Adjust x-axis label font size

# Adjust left axis tick font size
ax1.tick_params(axis='x', labelsize=13)  
ax1.tick_params(axis='y', labelsize=13)

# Right axis: Plot the injection volume scatter plot and rectangles
ax2 = ax1.twinx()
ax2.scatter(injection_data['Date'], injection_data['Average Rate'], color='#E2841D', s=20, label='Average Rate (m³/min)', zorder=5, alpha=0.7)

# Plot rectangles representing injection volume
for _, row in injection_data.iterrows():
    x = row['Date'] - pd.Timedelta(days=0.2)  # Bottom left corner
    y = row['Average Rate'] - row['Height'] / 2  # Height adjustment
    width = pd.Timedelta(days=0.4)  
    height = row['Height']
    
    rect = plt.Rectangle((x, y), width, height, facecolor='#E89D4A', edgecolor='w', alpha=0.4)
    ax2.add_patch(rect)

ax2.set_ylabel('Average Rate (m³/min)', fontsize=13)  # Adjust right axis label font size

# Adjust right axis tick font size
ax2.tick_params(axis='y', labelsize=16)

# Get both legend items
handles1, labels1 = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()

# Merge legends
ax1.legend(handles1 + handles2, labels1 + labels2, loc='upper left')

# Format time and adjust layout
fig.autofmt_xdate()
plt.tight_layout()
output_file = 'combined_plot_updated_v3.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
plt.show()

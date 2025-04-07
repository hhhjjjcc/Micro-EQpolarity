import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from datetime import datetime
import numpy as np
from obspy.imaging.beachball import beach

# -------------------------------
# Parse the timestamp, compatible with both versions with and without decimals
# -------------------------------
def parse_timestamp(ts):
    ts_str = str(ts).strip()  # Convert to string
    if '.' in ts_str:
        dt_obj = datetime.strptime(ts_str, '%Y%m%d%H%M%S.%f')
    else:
        dt_obj = datetime.strptime(ts_str, '%Y%m%d%H%M%S')
    return dt_obj.replace(microsecond=0)

# ==============================
# Read Excel data and generate datetime column
# ==============================
excel_file = './ToC2ME_Extract.xlsx'
df = pd.read_excel(excel_file)

# Ensure 'Second' is an integer to avoid time matching issues
df['Second'] = df['Second'].astype(int)
df['datetime'] = pd.to_datetime(df[['Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']])
df = df.sort_values(by='datetime')

# ==============================
# Read text data and process focal mechanism information
# ==============================
txt_file_path = './mt_solution_20250317_SKHASH_SWe_quality_A_B.txt'
df_txt = pd.read_csv(txt_file_path, sep='\t', header=None, 
                     names=['timestamp', 'lat_orig', 'lon_orig', 'depth', 'strike', 'dip', 'rake', 'flag'])

# Parse timestamp and ensure datetime is only to the second
df_txt['timestamp'] = df_txt['timestamp'].astype(str)  # Ensure it's a string
df_txt['datetime'] = df_txt['timestamp'].apply(parse_timestamp).dt.floor('S')

# Filter records where dip < 45°
df_txt_filtered = df_txt[df_txt['dip'] < 45].copy()

# ==============================
# Use merge_asof for time matching
# ==============================
df_match = df[['datetime', 'Latitude', 'Longitude']].sort_values('datetime')
df_merged = pd.merge_asof(df_txt_filtered.sort_values('datetime'), df_match, on='datetime', direction='nearest')

# **Print the actual focal mechanism records to be plotted**
print("### Actual Focal Mechanism Records to be Plotted ###")
print(df_merged)

# ==============================
# Set output directory and plot parameters
# ==============================
output_dir = './'
blue_color = '#737FBF'

# Specified fault times and corresponding titles
faults = [
    ('2016-11-20 19:58:31', 'Fault1 activation: 2016-11-20'),
    ('2016-11-21 22:26:46', 'Fault2 activation: 2016-11-21'),
    ('2016-11-22 05:21:40', 'Fault3 activation: 2016-11-22'),
    ('2016-11-22 19:45:47', 'Fault4 activation: 2016-11-22'),
    ('2016-11-23 06:45:35', 'Fault5 activation: 2016-11-23'),
    ('2016-11-24 04:42:07', 'Fault6 activation: 2016-11-24')
]

# ==============================
# Generate images for each fault time
# ==============================
for fault_time, title in faults:
    fault_datetime = pd.to_datetime(fault_time)
    
    # Only select Excel data before the fault time (for plotting scatter)
    current_data = df[df['datetime'] <= fault_datetime]
    
    # Focal mechanism balls **No time filtering, all mechanisms are plotted**
    current_mech = df_merged  # No time filtering here to ensure all dip < 45° mechanisms are displayed

    # Create Matplotlib figure
    fig, ax = plt.subplots(figsize=(8.27, 7))
    ax.set_xlabel('')
    ax.set_ylabel('')
    
    # Plot background scatter (light gray)
    ax.scatter(df['Longitude'], df['Latitude'], s=15, c='lightgray', alpha=0.5)
    # Plot data before the current fault time (blue)
    ax.scatter(current_data['Longitude'], current_data['Latitude'], s=15, c=blue_color)
    
    # --------------------------
    # Directly plot **all** focal mechanism balls
    # --------------------------
    for idx, row in current_mech.iterrows():
        mech = [row['strike'], row['dip'], row['rake']]
        lon, lat = row['Longitude'], row['Latitude']
        
        # Calculate the size of the focal mechanism ball (scale appropriately)
        size = 0.00015  # Scale appropriately to the longitude-latitude range
        
        # Create beachball and convert to Matplotlib Patch
        beachball_patch = beach(mech, xy=(lon, lat), width=size, linewidth=1, facecolor='#50AF71', edgecolor='k')
        
        # Add the focal mechanism ball directly to the ax
        ax.add_collection(beachball_patch)
    
    # Set plot title and axis labels
    ax.set_title(title, fontsize=20)
    ax.set_xlim(-117.230, -117.224)
    ax.set_xticks([-117.230, -117.228, -117.226, -117.224])
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
    
    # Save image
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = f'{output_dir}{title.split(":")[0]}.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

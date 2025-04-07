import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from obspy.imaging.beachball import beach
from matplotlib.ticker import FuncFormatter
import math

# Read the station list file
station_filename = './stationlist_ToC2ME.txt'
station_data = pd.read_csv(station_filename, delim_whitespace=True, header=None, names=['StationID', 'Network', 'Longitude', 'Latitude'])

# Extract station longitude and latitude
station_longitude = station_data['Longitude']
station_latitude = station_data['Latitude']

# Adjust negative longitudes by adding 360 degrees
station_longitude = station_longitude.apply(lambda x: x if x < 0 else x)

def read_mt_data(filenames):
    mt_data_list = []
    for filename in filenames:
        mt_data = pd.read_csv(
            filename,
            delim_whitespace=True,
            header=None,
            usecols=[1, 2, 3, 4, 5, 6, 8],
            names=['Latitude', 'Longitude', 'Depth', 'Strike', 'Dip', 'Rake', 'Magnitude']
        )
        mt_data['Group'] = os.path.basename(filename).split('_')[2]  # Extract group info from filename
        mt_data_list.append(mt_data)
    return pd.concat(mt_data_list, ignore_index=True)

# Read the focal mechanism file
mt_filenames = [
    './mt_solution_group1_20250319_with_mag.txt',
    './mt_solution_group2_20250319_with_mag.txt',
    './mt_solution_group3_20250319_with_mag.txt',
    './mt_solution_group4_20250319_with_mag.txt',
    './mt_solution_group_other_20250319_with_mag.txt'
]

mt_data = read_mt_data(mt_filenames)

# Adjust negative longitudes by adding 360 degrees
mt_data['Longitude'] = mt_data['Longitude'].apply(lambda x: x if x < 0 else x)

# Read the earthquake catalog data
#catalog_filename = '/home/jiachenhu/Desktop/Experiment16_ToC2ME_Independent_testing_20241016_from21916data/ToC2ME_catalog_all.xlsx'
catalog_filename = './ToC2ME.xlsx'

catalog_data = pd.read_excel(catalog_filename, usecols=[1, 2, 10, 4, 5, 6, 7, 8, 9], skiprows=1, names=['Latitude', 'Longitude', 'Magnitude', 'Year', 'Month', 'Day', 'Hour', 'Minute', 'Second'])

# Adjust negative longitudes by adding 360 degrees
catalog_data['Longitude'] = catalog_data['Longitude'].apply(lambda x: x if x < 0 else x)

# Create a figure window
plt.figure(figsize=(8.27, 6))

# Plot station locations, using black solid triangles
plt.scatter(station_longitude, station_latitude, c='k', marker='v', s=40)

# Plot earthquake locations, with a uniform gray color
plt.scatter(catalog_data['Longitude'], catalog_data['Latitude'], c='gray', s=3, alpha=0.3)

group_colors = {
    'group1': (1, 0, 0),       # Red
    'group2': (0, 0.8, 1),     # Light blue
    'group3': (0, 0.8, 0),     # Green
    'group4': (1, 0.7, 0),     # Orange
    'group': (1.0, 0.84, 0.0)  # Gold
}

for _, row in mt_data.iterrows():
    lon, lat = row['Longitude'], row['Latitude']

    # Beachball parameters
    mechanism = [row['Strike'], row['Dip'], row['Rake']]
    magnitude = row['Magnitude']
    group = row['Group']

    # Adjust size of beachball based on magnitude
    width = 0.0008699999999999999 + (magnitude * 0.00010999999999999999)  # Scales width dynamically with magnitude

    # Determine facecolor based on group
    facecolor = group_colors.get(group)  # Default to gray if group is unknown

    # Plot beachball
    b = beach(mechanism, xy=(lon, lat), width=width, facecolor=facecolor, linewidth=0.3, alpha = 0.8)
    b.set_zorder(10)
    plt.gca().add_collection(b)

# Function to read and directly connect latitude and longitude points
def plot_direct_curve(filepath):
    # Read file data
    data = pd.read_csv(filepath, delim_whitespace=True, header=None, names=['Latitude', 'Longitude'])
    
    # Adjust negative longitudes by adding 360 degrees
    data['Longitude'] = data['Longitude'].apply(lambda x: x if x < 0 else x)

    # Directly connect all points
    plt.plot(data['Longitude'], data['Latitude'], linewidth=1, color='black')

# Plot four curves
plot_direct_curve('./well-location-four.txt')
plot_direct_curve('./well-location-one.txt')
plot_direct_curve('./well-location-three.txt')
plot_direct_curve('./well-location-two.txt')

# Label the "Well numbers"
plt.text(-117.244249, 54.356307 - 0.0004, 'D', fontsize=20, ha='right', color='black', fontstyle='italic')
plt.text(-117.231989, 54.356307 - 0.0004, 'A', fontsize=20, ha='right', color='black', fontstyle='italic')
plt.text(-117.235955, 54.356307 - 0.0004, 'B', fontsize=20, ha='right', color='black', fontstyle='italic')
plt.text(-117.240282, 54.356307 - 0.0004, 'C', fontsize=20, ha='right', color='black', fontstyle='italic')
plt.text(-117.248216, 54.356307 - 0.0004, 'Well', fontsize=20, ha='right', color='black', fontstyle='italic')

# Set equal axis ratio to ensure Beachballs are circular
plt.axis('equal')

# Compute the central region's range (e.g., zoom in to 50% of the original range)
center_lon = (station_longitude.min() + station_longitude.max()) / 2
center_lat = (station_latitude.min() + station_latitude.max()) / 2
zoom_factor = 0.38  # Zoom to 50% range

plt.xticks(ticks=[-117.25, -117.24, -117.23, -117.22], labels=['-117.25', '-117.24', '-117.23', '-117.22'])
plt.yticks(ticks=[54.33, 54.34, 54.35, 54.36], labels=['54.33', '54.34', '54.35', '54.36'])

plt.xlim([center_lon - (center_lon - station_longitude.min()) * zoom_factor, 
          center_lon + (station_longitude.max() - center_lon) * zoom_factor])
plt.ylim([center_lat - (center_lat - station_latitude.min()) * zoom_factor, 
          center_lat + (station_latitude.max() - center_lat) * zoom_factor])
plt.tick_params(axis='both', which='major', labelsize=18)

# Ensure all borders are visible
plt.gca().spines['top'].set_visible(True)
plt.gca().spines['right'].set_visible(True)
plt.gca().spines['bottom'].set_visible(True)
plt.gca().spines['left'].set_visible(True)

# Save the figure
figname = './Station_Locations_with_Focal_Mechanisms_testing_data_2558events_gray.png'
plt.savefig(figname, bbox_inches='tight', dpi=300)

# Display the figure
plt.show()
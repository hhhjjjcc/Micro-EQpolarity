#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 11:20:11 2024

@author: jiachenhu
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from obspy.imaging.beachball import beach

def read_mt_solution(file_path):
    """Read solution file data"""
    column_names = ['evid', 'evla', 'evlo', 'depth', 'strike', 'dip', 'rake', 'misfit', 'magnitude']
    data = pd.read_csv(file_path, sep='\t', header=None, names=column_names)
    # Ensure 'evid' is of string type
    data['evid'] = data['evid'].astype(str)
    return data

def plot_direct_curve(filepath):
    """Read and plot well location curves"""
    # Read file data
    data = pd.read_csv(filepath, delim_whitespace=True, header=None, names=['Latitude', 'Longitude'])
    
    # Adjust negative longitudes by adding 360 degrees
    data['Longitude'] = data['Longitude'].apply(lambda x: x)
    # Directly connect all points
    plt.plot(data['Longitude'], data['Latitude'], linewidth=1, color='grey')


# Define file paths
file_paths = {
    'group_other': 'mt_solution_group_other_20250319_with_mag.txt',
    'group1': 'mt_solution_group1_20250319_with_mag.txt',
    'group2': 'mt_solution_group2_20250319_with_mag.txt',
    'group3': 'mt_solution_group3_20250319_with_mag.txt',
    'group4': 'mt_solution_group4_20250319_with_mag.txt',
}

# Define colors for each group
group_colors = {
    'group1': (1, 0, 0),      # Red
    'group2': (0, 0.8, 1),    # Light blue
    'group3': (0, 0.8, 0),    # Green
    'group4': (1, 0.7, 0),    # Orange
    'group_other': (1, 0.84, 0)  # Gold
}

# Create the figure
plt.figure(figsize=(8.27, 7))
ax = plt.gca()
ax.xaxis.set_major_formatter(FormatStrFormatter('%.3f'))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.3f'))

# Read and plot data for each group
line_length = 0.001  # Adjust the length of line segments
for group_name, file_path in file_paths.items():
    try:
        # Read data
        data = read_mt_solution(file_path)
        
        # Iterate over the data and plot
        for _, row in data.iterrows():
            evlo, evla = row['evlo'], row['evla']
            strike = row['strike']
            magnitude = row['magnitude']
            
            # Convert strike from clockwise from true north to counterclockwise from true east
            angle_rad = np.radians((90 - strike) % 360)
            dx = line_length * np.cos(angle_rad)
            dy = line_length * np.sin(angle_rad)
            
            # Plot the line segment representing the strike, using the group's color
            ax.plot([evlo - dx/2, evlo + dx/2], [evla - dy/2, evla + dy/2], 
                   color=group_colors[group_name], linewidth=1)
            
            # Plot a hollow circle at the center
            ax.scatter(evlo, evla, edgecolor='black', facecolor='none', s=30)
            
            # Only plot events with magnitude greater than 1.86
            if magnitude > 1.86:
                evlo, evla = row['evlo'], row['evla']
                strike, dip, rake = row['strike'], row['dip'], row['rake']

                # Adjust the size of the beachball based on the magnitude
                size = 0.00045 * magnitude

                # Generate the beachball
                b = beach([strike, dip, rake], xy=(evlo, evla), width=size, linewidth=1, facecolor=group_colors[group_name], alpha=0.8)
                ax.add_collection(b)

                # Mark the center of the beachball (optional)
                #ax.scatter(evlo, evla, edgecolor='black', facecolor='none', s=10)

    except Exception as e:
        print(f"Error processing {group_name}: {e}")

# Plot well location curves
plot_direct_curve('well-location-one.txt')
plot_direct_curve('well-location-two.txt')
plot_direct_curve('well-location-three.txt')
plot_direct_curve('well-location-four.txt')

# Label the "Well numbers"
plt.text(-117.244249 - 0.0006, 54.355307, 'D', fontsize=20, ha='right', color='grey', fontstyle='italic')
plt.text(-117.231989 - 0.0006, 54.355307, 'A', fontsize=20, ha='right', color='grey', fontstyle='italic')
plt.text(-117.235955 - 0.0006, 54.355307, 'B', fontsize=20, ha='right', color='grey', fontstyle='italic')
plt.text(-117.240282 - 0.0006, 54.355307, 'C', fontsize=20, ha='right', color='grey', fontstyle='italic')
plt.text(-117.248216 - 0.0006, 54.355307, 'Well', fontsize=20, ha='right', color='grey', fontstyle='italic')

longitude_ticks = [-117.250, -117.240, -117.230]
plt.gca().set_xticks(longitude_ticks)

plt.xticks(fontsize=22)
plt.yticks(fontsize=22)

# Add legend
legend_elements = [plt.Line2D([0], [0], color=color, label=group)
                  for group, color in group_colors.items()]
ax.legend(handles=legend_elements, loc='lower right', fontsize=20)

# Set axis labels
#plt.title('Focal Mechanisms by Group', fontsize = 24)

# Set equal axis ratio and adjust the display
plt.axis('equal')
plt.grid(False)
plt.tight_layout()

plt.savefig(f"Focal_Mechanisms_by_Group_with_Well_Locations_with_FMS.png", dpi=300, bbox_inches='tight', format='png')

# Show the plot
plt.show()
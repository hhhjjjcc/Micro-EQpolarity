#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 13:51:08 2024

@author: jiachenhu
"""

import os
import obspy
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import locale
import numpy as np
from matplotlib.gridspec import GridSpec

# Function to extract event dates and magnitudes from a dataset
def extract_event_data(base_dir):
    event_dates = []
    magnitudes = []
    for event_folder in os.listdir(base_dir):
        event_path = os.path.join(base_dir, event_folder)
        
        if os.path.isdir(event_path):
            # Get the first SAC file in the directory
            sac_files = [f for f in os.listdir(event_path) if f.endswith('.SAC')]
            if sac_files:
                sac_file_path = os.path.join(event_path, sac_files[0])
                # Use obspy to read the SAC file
                st = obspy.read(sac_file_path)
                sac_header = st[0].stats.sac
                
                # Extract magnitude information
                magnitude = sac_header['mag']
                
                # Parse EventID time
                event_id = event_folder
                year = int(event_id[:4])
                month = int(event_id[4:6])
                day = int(event_id[6:8])
                hour = int(event_id[8:10])
                minute = int(event_id[10:12])
                second = int(event_id[12:14])
                millisecond = int(event_id.split('.')[-1])
                
                # Construct event time as a datetime object
                event_time = datetime(year, month, day, hour, minute, second, millisecond * 1000)
                event_dates.append(event_time)
                magnitudes.append(magnitude)
    return event_dates, magnitudes

# Step 1: Read datasets
testing_base_dir = '/path/to/event_waveforms_for_SKHASH_2519'# See 'Data' part: ToC2ME 2519 FMSs waveforms: https://doi.org/10.5281/zenodo.15165318
training_base_dir = '/path/to/event_waveform_toc2me_me_2'  # See 'Data' part: ToC2ME all waveforms: https://doi.org/10.5281/zenodo.14185578

# Extract data
testing_event_dates, testing_magnitudes = extract_event_data(testing_base_dir)
training_event_dates, training_magnitudes = extract_event_data(training_base_dir)

# Calculate sizes
testing_sizes = [(mag + 3) * 8 for mag in testing_magnitudes]
training_sizes = [(mag + 3) * 8 for mag in training_magnitudes]

# Create figure with GridSpec
fig = plt.figure(figsize=(12, 6))
gs = GridSpec(1, 2, width_ratios=[3, 1.3], figure=fig)

# Create main scatter plot
ax1 = fig.add_subplot(gs[0])

# Create scatter plots
scatter1 = ax1.scatter(training_event_dates, training_magnitudes, 
                      s=training_sizes, c='orange', alpha=0.1, marker='o')
scatter2 = ax1.scatter(testing_event_dates, testing_magnitudes, 
                      s=testing_sizes, c='green', alpha=0.1, marker='o')

# Legend elements
legend_elements = [
    plt.scatter([], [], c='orange', alpha=0.7, marker='o', 
               label='All events (21619)', s=150),
    plt.scatter([], [], c='green', alpha=0.7, marker='o', 
               label='Resolved events (2519)', s=150)
]
ax1.legend(handles=legend_elements, fontsize=13)

# Format main plot
locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=5))
ax1.set_title("Magnitude Distribution", fontsize = 20)
ax1.set_xlabel("Date", fontsize = 16)
ax1.set_ylabel("Magnitude", fontsize = 16)
ax1.tick_params(axis='x', rotation=45, labelsize=14)  # Removed ha='right'
ax1.tick_params(axis='y',labelsize=14)
plt.setp(ax1.get_xticklabels(), ha='right')  # Set horizontal alignment separately
ax1.grid(color='lightgray', linestyle='--', alpha=0.5)

# Create histogram subplot
ax2 = fig.add_subplot(gs[1], sharey=ax1)

# Combine all magnitudes
all_magnitudes = training_magnitudes + testing_magnitudes

# Create magnitude bins with 0.1 intervals
magnitude_range = np.arange(min(all_magnitudes) - 0.05, max(all_magnitudes) + 0.15, 0.1)
counts_training, _ = np.histogram(training_magnitudes, bins=magnitude_range)
counts_testing, _ = np.histogram(testing_magnitudes, bins=magnitude_range)

# Plot horizontal histogram
ax2.barh(magnitude_range[:-1] + 0.05, counts_training, height=0.08, 
         color='orange', alpha=0.7, label='All events (21619)')
ax2.barh(magnitude_range[:-1] + 0.05, counts_testing, height=0.08, 
         color='green', alpha=0.7, label='Resolved events (2519)')

ax2.set_title("Event Distribution", fontsize = 20)
ax2.set_xlabel("Number of Events",fontsize = 16)
ax2.tick_params(axis='x', labelsize=14) 
ax2.tick_params(axis='y', labelsize=14)
ax2.grid(color='lightgray', linestyle='--', alpha=0.5)
ax2.legend(fontsize=13)

# Remove y-axis labels for the histogram since it shares with main plot
#ax2.set_yticklabels([])

# Adjust layout
plt.tight_layout()

# Save and show
plt.savefig("magnitude_vs_time_with_distribution.png", dpi=300, bbox_inches='tight')
plt.show()

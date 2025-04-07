#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 17:46:36 2024

@author: jiachenhu
"""

import numpy as np
import matplotlib.pyplot as plt
from obspy.imaging.beachball import beach
from matplotlib.patches import Circle

# File path
file_path = "mt_solution_group_other_20250319.txt"

# Read the data
events = []
with open(file_path, 'r') as f:
    for line in f:
        parts = line.split()
        event_id = parts[0]
        latitude = float(parts[1])
        longitude = float(parts[2])
        depth = float(parts[3])
        strike = int(parts[4])
        dip = int(parts[5])
        rake = int(parts[6])
        rms = float(parts[7])
        
        events.append({"event_id": event_id, "strike": strike, "dip": dip, "rake": rake})

# Output the number of events
print(f"Total number of events read: {len(events)}")

# Prepare for plotting
fig, ax = plt.subplots(figsize=(6, 6))  # Set figure size to 6x6 inches

# 添加黑色圆圈作为底图
circle = Circle((0, 0), 1, fill=False, color='black', linewidth=1.0, zorder=1)
ax.add_patch(circle)

# Loop through and plot each event
for i, event in enumerate(events):
    strike = event['strike']
    dip = event['dip']
    rake = event['rake']
    b = beach([strike, dip, rake], xy=(0, 0), width=2, linewidth=0.5, facecolor='none', edgecolor='#FFD700', nofill=True, zorder=0)
    ax.add_collection(b)

# Set plot parameters
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal')
ax.axis('off')

# Dynamically generate the output filename
output_base = f"mt_solution_strike_rake_group2_beachballs_{len(events)}"

# Save the image at 300 DPI in both EPS and PNG formats
plt.savefig(f"{output_base}.png", dpi=300, bbox_inches='tight', format='png')

# Display the image
plt.show()

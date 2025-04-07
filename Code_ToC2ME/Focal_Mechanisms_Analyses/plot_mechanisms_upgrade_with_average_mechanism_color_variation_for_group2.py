#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 17:46:36 2024

@author: jiachenhu
"""

import numpy as np
import matplotlib.pyplot as plt
from obspy.imaging.beachball import beach
from datetime import datetime
import matplotlib.patches as patches

def stereonet_projection(strike, dip):
    """
    Convert strike and dip to stereonet projection x, y coordinates
    Parameters:
    strike: Strike (degrees)
    dip: Dip (degrees)
    Returns:
    x, y: Projected coordinates
    """
    # Convert degrees to radians
    strike_rad = np.radians(strike)
    dip_rad = np.radians(dip)
    
    # Calculate projected coordinates
    r = np.tan(np.pi/4 - dip_rad/2)
    x = r * np.sin(strike_rad)
    y = r * np.cos(strike_rad)
    
    return x, y

# File path
file_path = "./mt_solution_group2_20250319.txt"

# Generate dynamic filename
fault_type = "strike_slip_fault"

# Set standard deviation threshold
std_threshold = 100

# Read data
events = []
with open(file_path, 'r') as f:
    for line in f:
        parts = line.split()
        event_id = parts[0]
        latitude = float(parts[1])
        longitude = float(parts[2])
        depth = float(parts[3])
        strike = float(parts[4])  # Changed to float
        dip = float(parts[5])     # Changed to float
        rake = float(parts[6])    # Changed to float
        rms = float(parts[7])
        
        events.append({
            "event_id": event_id,
            "strike": strike,
            "dip": dip,
            "rake": rake
        })

# Output number of events
print(f"Total number of events read: {len(events)}")

# Calculate averages
adjusted_strikes = [
    event['strike'] - 360 if event['strike'] > 355 else 
    (event['strike'] - 180 if event['strike'] > 170 else event['strike'])
    for event in events
]
avg_strike = np.mean(adjusted_strikes)
std_strike = np.std(adjusted_strikes)
avg_dip = np.mean([event['dip'] for event in events])
std_dip = np.std([event['dip'] for event in events])
avg_rake = np.mean([abs(event['rake']) for event in events])
std_rake = np.std([abs(event['rake']) for event in events])

# Print averages and standard deviations
print(f"Average Strike: {avg_strike:.2f}, Standard Deviation: {std_strike:.2f}")
print(f"Average Dip: {avg_dip:.2f}, Standard Deviation: {std_dip:.2f}")
print(f"Average Rake: {avg_rake:.2f}, Standard Deviation: {std_rake:.2f}")

# Filter events
filtered_events = [
    event for event in events
    if (avg_strike - std_threshold * std_strike <= (event['strike'] - 360 if event['strike'] > 355 else 
        (event['strike'] - 180 if event['strike'] > 170 else event['strike'])) <= avg_strike + std_threshold * std_strike) and
       (avg_dip - std_threshold * std_dip <= event['dip'] <= avg_dip + std_threshold * std_dip) and
       (avg_rake - std_threshold * std_rake <= abs(event['rake']) <= avg_rake + std_threshold * std_rake)
]

# Print the number of filtered events
print(f"Number of filtered events: {len(filtered_events)}")

# Extract filtered values
if filtered_events:
    strikes_filter = np.array([(event['strike'] - 360 if event['strike'] > 355 else 
                              (event['strike'] - 180 if event['strike'] > 170 else event['strike'])) 
                             for event in filtered_events])
    dips_filter = np.array([event['dip'] for event in filtered_events])
    rakes_filter = np.array([abs(event['rake']) for event in filtered_events])
    
    avg_strike_filter = np.mean(strikes_filter)
    std_strike_filter = np.std(strikes_filter)
    avg_dip_filter = np.mean(dips_filter)
    std_dip_filter = np.std(dips_filter)
    avg_rake_filter = np.mean(rakes_filter)
    std_rake_filter = np.std(rakes_filter)
    
    # Print filtered averages and standard deviations
    print(f"Filtered Average Strike: {avg_strike_filter:.2f}, Standard Deviation: {std_strike_filter:.2f}")
    print(f"Filtered Average Dip: {avg_dip_filter:.2f}, Standard Deviation: {std_dip_filter:.2f}")
    print(f"Filtered Average Rake: {avg_rake_filter:.2f}, Standard Deviation: {std_rake_filter:.2f}")
else:
    print("No events meet the criteria.")

# Prepare the plot
plt.figure(figsize=(6, 6))  # Increase figure size
plt.tight_layout()  # Optimize layout

# Add black circular boundary
circle = patches.Circle((0, 0), radius=1, fill=False, color='black', linewidth=1.5, zorder=1)
plt.gca().add_patch(circle)

# Plot average focal mechanism
b_avg = beach(
    [avg_strike_filter, avg_dip_filter, avg_rake_filter], xy=(0, 0), width=2, linewidth=1.0,
    facecolor='grey', edgecolor='black', zorder=0, alpha=0.3 
)
plt.gca().add_collection(b_avg)

# Calculate deviation for each event and find the maximum deviation
deviations = [abs(event['strike'] - avg_strike_filter) for event in filtered_events]
max_deviation = max(deviations)

# Plot each event's Beachball and set color and transparency based on deviation from avg_strike_filter
for event in filtered_events:
    deviation = abs(event['strike'] - avg_strike_filter)
    normalized_deviation = min(deviation / 20, 1)  # Normalize deviation to [0, 1]
    
    # Color from Red to white, greater deviation means whiter
    color = (normalized_deviation, 0.8, 1)  # RGB color definition
    
    # Transparency increases as deviation decreases
    alpha = 0.3 * (1 - normalized_deviation)  # Larger deviation, smaller alpha
    
    # Create Beachball
    b = beach(
        [event['strike'], event['dip'], event['rake']], xy=(0, 0), width=2,
        linewidth=0.5, facecolor='none', edgecolor=color, nofill=True,
        alpha=alpha, zorder=-1
    )
    plt.gca().add_collection(b)

# For Stress
# Sigma 1
x1, y1 = stereonet_projection(251, 1)
plt.scatter(x1, y1, color='purple', marker='o', s=200, edgecolor='black', linewidth=1, zorder=5)

# Sigma 2
x2, y2 = stereonet_projection(34, 89)
plt.scatter(x2, y2, color='green', marker='s', s=200, edgecolor='black', linewidth=1, zorder=5)

# Sigma 3
x3, y3 = stereonet_projection(161, 1)
plt.scatter(x3, y3, color='yellow', marker='^', s=200, edgecolor='black', linewidth=1, zorder=5)

# Add legend
legend_elements = [
    plt.scatter([], [], color='purple', edgecolor='black', linewidth=1, marker='o', s=100, label='σ1 (251°/1°)'),
    plt.scatter([], [], color='green', edgecolor='black', linewidth=1, marker='s', s=100, label='σ2 (34°/89°)'),
    plt.scatter([], [], color='yellow', edgecolor='black', linewidth=1, marker='^', s=100, label='σ3 (161°/1°)')
]

plt.legend(
    handles=legend_elements,
    loc='lower center',  # Move legend to bottom center
    bbox_to_anchor=(0.5, -0.2),  # Adjust legend position for vertical arrangement
    fontsize=20,  # Increase font size
    ncol=1,  # Single column display
    frameon=True,  # Show legend border
    bbox_transform=plt.gca().transAxes
)

# Set coordinates
plt.xlim(-1.5, 1.5)
plt.ylim(-1.5, 1.5)
plt.gca().set_aspect('equal')
plt.axis('off')

# Generate timestamp
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f"./{fault_type}_beachball_plot_std_{std_threshold}_NE_SW_{current_time}.png"

# Save the figure, removing extra margins
plt.savefig(output_filename, dpi=300, bbox_inches='tight')
print(f"Figure saved as: {output_filename}")

# Display the figure
plt.show()

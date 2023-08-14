# Solar Tracker Optimization

# This script performs solar tracker optimization for a photovoltaic (PV) system.
# The main goal is to find optimal tracker angles that minimize shadowing and maximize solar exposure.

# Import necessary libraries
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from pvlib.tools import cosd, sind, tand
from pvlib import solarposition, tracking
from scipy.optimize import minimize

# Location parameters
tz = 'US/Eastern'
lat, lon = 20, -80
separation = 6
slope_azimuth = [0, 0, 0]
slope_tilt = [0, 15, -15]
axis_azimuth = 180  # tracker axis is still N-S
tracker_height = 2
module_pv_height = 2
optimal_tracker_angles = []
method = 'L-BFGS-B'
results = []
tracker_angle_1 = []
tracker_angle_2 = []
tracker_angle_3 = []

# Period time
times = pd.date_range('2023-01-01 06:30', '2023-01-01 12:00', freq='15min', tz=tz)

solpos = solarposition.get_solarposition(times, lat, lon)
df = pd.DataFrame(solpos)

# Define a function to calculate solar angles in XYZ tracking system
def solar_xyz_trayec(apparent_zenith, apparent_azimuth, slope_azimuth, slope_tilt):
    """
    Calculate solar angles in XYZ tracking system.

    Input:
    apparent_zenith (pd.Series): Apparent solar zenith angles in degrees.
    apparent_azimuth (pd.Series): Apparent solar azimuth angles in degrees.
    slope_azimuth (float): Azimuth angle of the PV panel slope in degrees.
    slope_tilt (float): Tilt angle of the PV panel slope in degrees.

    Output:
    solar_angle (pd.Series): Solar angles in degrees in the XYZ tracking system.
    """

    axis_tilt = tracking.calc_axis_tilt(slope_azimuth, slope_tilt, axis_azimuth)
    cos_axis_azimuth = cosd(axis_azimuth)
    sin_axis_azimuth = sind(axis_azimuth)
    cos_axis_tilt = cosd(axis_tilt)
    sin_axis_tilt = sind(axis_tilt)
    sin_zenith = sind(apparent_zenith)
    x = sin_zenith * sind(apparent_azimuth)
    y = sin_zenith * cosd(apparent_azimuth)
    z = cosd(apparent_zenith)
    xp = x*cos_axis_azimuth - y*sin_axis_azimuth
    zp = (x*sin_axis_tilt*sin_axis_azimuth + y*sin_axis_tilt*cos_axis_azimuth + z*cos_axis_tilt)
    solar_angle = np.degrees(np.arctan2(xp, zp))
    zen_gt_90 = apparent_zenith > 90
    solar_angle[zen_gt_90] = np.nan
    solar_angle = solar_angle.fillna(0)
    return solar_angle

# Define a function to calculate shadow lengths
def shadow(solar_angle_1, tracker_height, module_pv_height, tracker_angle_1, tracker_angle_2, tracker_angle_3, separation, time_idx):
    """
    Calculate shadow lengths for a given solar angle and tracker configuration.

    Input:
    solar_angle_1 (pd.Series): Solar angles in degrees.
    tracker_height (float): Height of the solar tracker above ground in meters.
    module_pv_height (float): Height of the PV module above the tracker in meters.
    tracker_angle_1 (float): Tracker angle 1 in degrees.
    tracker_angle_2 (float): Tracker angle 2 in degrees.
    tracker_angle_3 (float): Tracker angle 3 in degrees.
    separation (float): Separation between modules in meters.
    time_idx (int): Index of the time step.

    Output:
    shadow_lengths (float): Shadow lengths calculated based on the given parameters.
    """
    separation_correction = separation - np.cos((tracker_angle_2))*module_pv_height/2
    object_height = tracker_height + (module_pv_height/np.sin((tracker_angle_1)))
    shadow = object_height / math.tan(solar_angle_1[time_idx])

    if (separation_correction - shadow) > 0:
        shadow_lengths = -10
    else:
        shadow_lengths = 1
    return shadow_lengths




# Define a function to optimize tracker angles
def optimize_tracker_angle(f, time_idx):
    """
    Optimize tracker angles to minimize shadowing and maximize solar exposure.

    Input:
    f (tuple): Tuple containing tracker angles (tracker_angle_1, tracker_angle_2, tracker_angle_3) in degrees.
    time_idx (int): Index of the time step.

    Output:
    objective (float): Objective value representing the sum of shadow lengths and differences in solar angles.
    """
    tracker_angle_1, tracker_angle_2, tracker_angle_3 = f
    df["solar_angle_1"] = solar_xyz_trayec(solpos['apparent_zenith'],solpos['azimuth'],slope_azimuth[0],slope_tilt[0])
    df["solar_angle_2"] = solar_xyz_trayec(solpos['apparent_zenith'],solpos['azimuth'],slope_azimuth[1],slope_tilt[1])
    df["solar_angle_3"] = solar_xyz_trayec(solpos['apparent_zenith'],solpos['azimuth'],slope_azimuth[2],slope_tilt[2])
    solar_angle_1 = df["solar_angle_1"]
    solar_angle_2 = df["solar_angle_2"] 
    solar_angle_3 = df["solar_angle_3"] 
    diff_angles = np.abs(solar_angle_1[time_idx] - tracker_angle_1) + np.abs(solar_angle_2[time_idx] - tracker_angle_2) + np.abs(solar_angle_3[time_idx] - tracker_angle_3) 
    shadow_lengths = [shadow(solar_angle_1, tracker_height, module_pv_height, tracker_angle_1, tracker_angle_2, tracker_angle_3, separation,time_idx)]
    print((shadow_lengths), "Sombra")
    print((diff_angles), "Diferencia angulos")
    print(shadow_lengths+diff_angles), "Suma de los 2"
    return shadow_lengths+diff_angles

# Iterate over each time index
for time_idx in range(len(times)):
    initial_guess = [0, 0, 0] 
    result = minimize(optimize_tracker_angle, initial_guess, args=(time_idx,),bounds=[(-60, 60), (-60, 60),(-60, 60)], method=method)
    optimal_tracker_angles = result.x 
    # Append the result to the list of results
    results.append(optimal_tracker_angles)

# Append the list of results to optimal_tracker_angles list
optimal_tracker_angles = results

optimal_tracker_angles = np.array(optimal_tracker_angles)

# Plot the optimized tracker angles
plt.figure(figsize=(10, 6))
plt.plot(times, optimal_tracker_angles[:, 0], label='Tracker Angle 1')
plt.plot(times, optimal_tracker_angles[:, 1], label='Tracker Angle 2')
plt.plot(times, optimal_tracker_angles[:, 2], label='Tracker Angle 3')
plt.plot(times, df['solar_angle_1'], label='Solar Angle 1', linestyle='dashed')
plt.plot(times, df['solar_angle_2'], label='Solar Angle 2', linestyle='dashed')
plt.plot(times, df['solar_angle_3'], label='Solar Angle 3', linestyle='dashed')
plt.xlabel('Time')
plt.ylabel('Angles (degrees)')
plt.title('Optimized Tracker Angles and Solar Angles Over Time')
plt.legend()
plt.grid()
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot
plt.show()
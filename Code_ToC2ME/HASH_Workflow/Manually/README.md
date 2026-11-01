# Manual Polarity Picking (MATLAB GUI)

## Description

This folder provides a MATLAB GUI for manually picking P-wave first-motion polarities. It is the manual alternative to the automatic EQpolarity workflow in `../Automatically_EQpolarity/`.

## MATLAB Waveform Picking Steps Summary

1. **Run `polarity_picking.m`**
   - Open the script and run it to enter the main interface.

2. **Load Data**
   - Click the **Load data** button to load the required waveform data.

3. **Mark P-wave Arrival**
   - Click **Mark P arrival**, and a red line will appear in the interface.

4. **Adjust View**
   - Based on the red line position, input `t0` and `t1` to zoom in on the waveform near the red line.
   - Click **Set xlim** to set the x-axis range.

5. **Determine Waveform Polarity**
   - Observe the **vertical** plot (the top waveform plot) and determine whether the waveform to the right of the red line moves upward or downward:
     - If downward, click **Down**.
     - If upward, click **Up**.
     - Click **Next** to move to the next trace.

6. **Complete Polarity Picking for All Stations**
   - For each station, determine the waveform polarity (`Up` or `Down`).
   - Once all stations are processed, click **Finish** to complete.

---

## Output Results

- Results are saved in the `matlab_GUI_v0.5/output/` folder.
- The `matlab_GUI_v0.5/output/` folder contains a runnable example for event `20161104064824.680`.
- You can use these outputs to run SKHASH. See the `../Automatically_EQpolarity/README.md` workflow for the downstream steps.
- The `matlab_GUI_v0.5/sp_ratio/energy_cyf.py` helper is a legacy Texas-data utility; its example file paths are relative placeholders — point them to local waveform, catalog, station, and model files before use.

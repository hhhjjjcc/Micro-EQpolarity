# Plot Waveforms on Focal Mechanisms

## Description

This folder validates a focal mechanism solution by plotting its beachball together with station projections and the corresponding P-wave waveforms.

## Folder Contents

- `Focal_mechanism_with_waveform_20241117_skhash.py`: main plotting script (all paths are relative to this folder).
- `mt_solution_20250317_SKHASH_quality_A.txt`: focal mechanism list used by the script (`event_id latitude longitude depth strike dip rake`).
- `out_polinfo.csv`: SKHASH polarity/ray information (`event_id`, `sta_code`, `azimuth`, `takeoff`, `p_polarity`) used for the station projections.
- `data_demo/20161125094237.760/`: demo three-component SAC waveforms for the example event (`*DHZ.SAC` traces are plotted).
- `focal_mechanism_21034_Strike_Slip_Fault.png`: example output figure for event `20161125094237.760` (SKHASH id `21034`).

## How to Run

Run the script from this folder:

```bash
python Focal_mechanism_with_waveform_20241117_skhash.py
```

The script reads `./mt_solution_20250317_SKHASH_quality_A.txt`, `./out_polinfo.csv`, and `./data_demo/<event_id>/`, and writes `focal_mechanism_<SKHASH_id>_<fault_type>.png` into this folder.

## Notes

- In the ToC2ME dataset, waveform polarities are inverted.
- All file paths are relative; no absolute paths are required.

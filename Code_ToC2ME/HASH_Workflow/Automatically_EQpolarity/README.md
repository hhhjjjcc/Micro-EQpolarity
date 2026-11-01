# SKHASH Workflow (Automatic Polarity Picking)

## Description

This folder provides the automatic workflow for solving focal mechanisms with SKHASH on the ToC2ME dataset. P-wave first-motion polarities are predicted with the trained Micro-EQpolarity model and then converted into SKHASH inputs.

## Folder Contents

- `run_eqpolarity_ToC2ME.ipynb`: loads the trained Micro-EQpolarity weights with a relative path (`../../../model/Toc2me_20240819_Transfer_Learning_21916data/best_weigths_Binary_Toc2me_Transfer_SCSN_20241013_21916data_90.h5`), reads waveforms listed in `../all_data_demo/catalog_sorted_ToC2ME.txt`, and writes one `.polarity` file per event into `./result_ToC2ME_eqpolarity/`. Station coordinates are read from SAC headers in this workflow.
- `generate_catalog.py`: lists event folders in `../all_data_demo` (directories only) and writes `../all_data_demo/catalog_sorted_ToC2ME.txt`.
- `filter_polarity_average_pol.py`: reads `./result_ToC2ME_eqpolarity` and keeps confident picks with `abs(polarity - 0.5) >= 0.45` (i.e. polarities near 0 or 1) into `./results_ToC2ME_eqpolarity_filtered_pol_average/`.
- `generate_pol_hash_for_independent_test.m`: converts `.polarity` files into `.pol.hash` files using SAC data in `../all_data_demo`.
- `Reverse_pol_hash_polarity.py`: reverses `+`/`-` signs in `./result_ToC2ME_pol_hash_auto/` (required for the ToC2ME dataset because of the instrument installation).
- `SNR_from_event_waveform_toc2me_me_2.py`: computes SNR for every waveform in `../all_data_demo` and saves `SNR_event_waveform_toc2me_me_2.csv` in this folder.
- `delete_low_SNR_waveform_in_pol_hash.py`: removes station records with SNR <= 2 (based on `SNR_event_waveform_toc2me_me_2.csv`) from the `.pol.hash` files in `./result_ToC2ME_pol_hash_auto/`.
- `generate_eq_catalog.py` / `generate_pol_csv.py`: build `SKHASH/SKHASH/ToC2ME_demo/IN/SKHASH.eq_catalog.csv` and `SKHASH/SKHASH/ToC2ME_demo/IN/SKHASH.pol.csv` from the `.pol.hash` files.
- `../all_data_demo/`: demo waveforms (3 sample events), `catalog_sorted_ToC2ME.txt`, and `stationlist_ToC2ME.txt` (`station_id network longitude latitude`).
- `SKHASH/`: SKHASH solver with the `SKHASH/SKHASH/ToC2ME_demo/` example (control file, velocity model, input and output CSV files).
- `MatSAC/`: MATLAB SAC I/O utilities.

## How to Run

### Step 1

Run `generate_catalog.py` to generate the `catalog_sorted_ToC2ME.txt` file in the `../all_data_demo` folder.

### Step 2

Run the `run_eqpolarity_ToC2ME.ipynb` notebook to obtain one `.polarity` file per event in the `./result_ToC2ME_eqpolarity` folder.

### Step 3

Run `filter_polarity_average_pol.py` to keep only confident picks (`abs(polarity - 0.5) >= 0.45`) from the `./result_ToC2ME_eqpolarity` folder into `./results_ToC2ME_eqpolarity_filtered_pol_average/`.

### Step 4

Run `generate_pol_hash_for_independent_test.m` to generate the `.pol.hash` files in `./result_ToC2ME_pol_hash_auto/`.

### Step 5

For the ToC2ME dataset, run `Reverse_pol_hash_polarity.py` to reverse the polarity signs because of the instrument installation.

### Step 6

Run `SNR_from_event_waveform_toc2me_me_2.py` to calculate the signal-to-noise ratio (SNR) for all waveform files in the `../all_data_demo` folder and save the results in `SNR_event_waveform_toc2me_me_2.csv`.

### Step 7

Run `delete_low_SNR_waveform_in_pol_hash.py` to remove station records with an SNR of 2 or less from the `.pol.hash` files.

### Step 8

Follow the instructions in the `SKHASH` folder `README.md` to solve focal mechanisms with SKHASH. The helper scripts `generate_eq_catalog.py` and `generate_pol_csv.py` transform `.pol.hash` files into the SKHASH inputs:

- `generate_eq_catalog.py`: generates the `SKHASH.eq_catalog.csv` control-file input from the `.pol.hash` files.
- `generate_pol_csv.py`: generates the `SKHASH.pol.csv` control-file input from the `.pol.hash` files.

Run the following command in the terminal:

```bash
python3 SKHASH.py ToC2ME_demo/control_file_skhash.txt
```

All paths in this workflow are relative; no absolute paths are required.

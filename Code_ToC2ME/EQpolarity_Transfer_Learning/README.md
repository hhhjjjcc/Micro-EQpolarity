# EQpolarity Transfer Learning

## Description

This folder contains the transfer-learning workflow that adapts the EQpolarity model to ToC2ME microseismic data (Micro-EQpolarity), plus a lightweight inference demo.

## Folder Contents

- `CCT_ToC2ME_TransferLearning_20240926_For_Test_update20241013.ipynb`: full training and evaluation notebook (training/validation curves, precision-recall and ROC curves, and the model comparison on the ToC2ME test set).
- `run_eqpolarity_ToC2ME.ipynb`: inference demo. It loads the trained weights with a relative path (`../../model/Toc2me_20240819_Transfer_Learning_21916data/best_weigths_Binary_Toc2me_Transfer_SCSN_20241013_21916data_90.h5`), reads the demo events listed in `../HASH_Workflow/all_data_demo/catalog_sorted_ToC2ME.txt` together with station coordinates from `../HASH_Workflow/all_data_demo/stationlist_ToC2ME.txt` (`station_id network longitude latitude`), and writes one `.polarity` file per event into `./result_ToC2ME_eqpolarity/` (created automatically if missing).
- `Training_Validation_curves.py`: reproduces `training_validation_loss.png` and `training_validation_accuracy.png` from `training_log_90.csv`.
- `training_log_90.csv`: training log of the best (epoch 9) Micro-EQpolarity run.
- `result_ToC2ME_eqpolarity/`: output folder for the inference demo (one `.polarity` file per event; columns are `station_id evla evlo evdp stla stlo polarity`).
- Evaluation figures: `training_validation_loss.png`, `training_validation_accuracy.png`, `confusion_matrix.png`, `precision_recall_curves_ToC2ME.png`, `roc_curves_ToC2ME.png`, `Model_Comparison_on_Microseismic_Events.png`.
- `run_eqpolarity_transferlearning_Texas_10percent.ipynb`: reference fine-tuning demo on Texas data (kept for reference; not part of the ToC2ME run).

## How to Run the Inference Demo

1. Make sure the demo data exist in `../HASH_Workflow/all_data_demo/` (`catalog_sorted_ToC2ME.txt`, `stationlist_ToC2ME.txt`, and the event waveform folders).
2. Open `run_eqpolarity_ToC2ME.ipynb` and run all cells. No path editing is needed; all paths are relative.
3. Collect the per-event `.polarity` files from `./result_ToC2ME_eqpolarity/`.

## Notes

- All file paths in this folder are relative; no absolute paths are used.
- The `530events` / `result_530events` names from earlier experiments are no longer used. The demo now uses `all_data_demo` and `result_ToC2ME_eqpolarity`.

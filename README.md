# Industrial IoT Predictive Maintenance Platform

Predictive maintenance platform for wind turbines using real SCADA data (CARE to Compare V6).

## Status
Phase 0 (dataset exploration) completed. Phase 1 in progress.

## Structure
- `data/` raw/interim/processed (raw excluded from git)
- `notebooks/` exploration and training notebooks (runnable in Colab)
- `reports/` audit reports and inventories
- `docs/` project overview, architecture, roadmap, tech stack
- `src/` ingestion and utilities

## Setup (local)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Notebooks in Colab
Notebooks are designed to run in Google Colab. Set the dataset path in the
configuration cell. For Colab, upload the extracted `CARE_To_Compare/` folder
or mount Google Drive, then point `DATASET_DIR` accordingly.

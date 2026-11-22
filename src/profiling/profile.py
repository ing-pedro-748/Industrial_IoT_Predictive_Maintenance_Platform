"""Batch profiling of all CARE to Compare V6 dataset files."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

from src.utils.data_loader import DatasetSource
from src.validation.data_quality import timestamp_continuity, constant_columns


def profile_one(source: DatasetSource, rel: str) -> Dict:
    df = source.read_csv(rel, sep=";")
    gaps = timestamp_continuity(df)
    status_counts = df["status_type_id"].value_counts().to_dict() if "status_type_id" in df.columns else {}
    train_counts = df["train_test"].value_counts().to_dict() if "train_test" in df.columns else {}
    nulls = df.isna().sum()
    return {
        "file": rel,
        "farm": rel.split("/")[0] if "/" in rel else "",
        "asset_id": int(df["asset_id"].iloc[0]) if "asset_id" in df.columns else None,
        "n_rows": int(len(df)),
        "n_cols": int(df.shape[1]),
        "total_nulls": int(nulls.sum()),
        "null_cols": int((nulls > 0).sum()),
        "constant_cols": len(constant_columns(df)),
        "n_gaps": int(len(gaps)),
        "max_gap_minutes": float(gaps["gap"].max().total_seconds() / 60) if len(gaps) else 0.0,
        "status_counts": {str(k): int(v) for k, v in status_counts.items()},
        "train_counts": {str(k): int(v) for k, v in train_counts.items()},
    }


def profile_all(source: DatasetSource) -> pd.DataFrame:
    files = sorted(source.list_files(".csv"))
    dataset_files = [f for f in files if "datasets" in f.replace(chr(92), "/")]
    records: List[Dict] = []
    for i, rel in enumerate(dataset_files, 1):
        print(f"[{i}/{len(dataset_files)}] {rel}", flush=True)
        try:
            records.append(profile_one(source, rel))
        except Exception as e:
            records.append({"file": rel, "error": str(e)})
    return pd.DataFrame(records)

"""Data quality validation helpers for CARE to Compare V6."""
from __future__ import annotations

from typing import Dict, List

import numpy as np
import pandas as pd


def null_report(df: pd.DataFrame) -> pd.DataFrame:
    nulls = df.isna().sum()
    out = pd.DataFrame({"column": nulls.index, "null_count": nulls.values})
    out["null_ratio"] = out["null_count"] / len(df)
    return out[out["null_count"] > 0].sort_values("null_count", ascending=False)


def duplicate_report(df: pd.DataFrame) -> Dict[str, int]:
    return {
        "duplicate_rows": int(df.duplicated().sum()),
        "duplicate_timestamps": int(df["time_stamp"].duplicated().sum()) if "time_stamp" in df.columns else 0,
        "duplicate_ids": int(df["id"].duplicated().sum()) if "id" in df.columns else 0,
    }


def timestamp_continuity(df: pd.DataFrame, freq_minutes: int = 10) -> pd.DataFrame:
    """Return gaps larger than the expected sampling frequency."""
    ts = pd.to_datetime(df["time_stamp"])
    deltas = ts.diff()
    threshold = pd.Timedelta(minutes=freq_minutes)
    mask = deltas > threshold
    gaps = pd.DataFrame({
        "index": df.index[mask],
        "prev_time": ts.shift(1)[mask].values,
        "curr_time": ts[mask].values,
        "gap": deltas[mask].values,
    })
    return gaps.reset_index(drop=True)


def constant_columns(df: pd.DataFrame) -> List[str]:
    num = df.select_dtypes(include=[np.number])
    return [c for c in num.columns if num[c].nunique(dropna=False) <= 1]


def zero_counts(df: pd.DataFrame) -> pd.DataFrame:
    num = df.select_dtypes(include=[np.number])
    zc = (num == 0).sum()
    out = pd.DataFrame({"column": zc.index, "zero_count": zc.values})
    out["zero_ratio"] = out["zero_count"] / len(df)
    return out[out["zero_count"] > 0].sort_values("zero_count", ascending=False)


def basic_validation(df: pd.DataFrame) -> Dict[str, object]:
    return {
        "shape": df.shape,
        "nulls": null_report(df).to_dict("records"),
        "duplicates": duplicate_report(df),
        "constant_columns": constant_columns(df),
        "inf_count": int(np.isinf(df.select_dtypes(include=[np.number])).sum().sum()),
    }

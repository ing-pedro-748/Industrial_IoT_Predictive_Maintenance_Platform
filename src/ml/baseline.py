"""Statistical anomaly detection baselines."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

from src.utils.data_loader import DatasetSource


def load_series(source: DatasetSource, farm: str, event_id: int, asset_id: Optional[int] = None) -> pd.DataFrame:
    rel = f"Wind Farm {farm}/datasets/{event_id}.csv"
    df = source.read_csv(rel, sep=";")
    df["time_stamp"] = pd.to_datetime(df["time_stamp"])
    if asset_id is not None:
        df = df[df["asset_id"] == asset_id].copy()
    return df.sort_values("time_stamp").reset_index(drop=True)


def add_event_labels(df: pd.DataFrame, event_info: pd.DataFrame, event_id: int) -> pd.DataFrame:
    ev = event_info[event_info["event_id"] == event_id].iloc[0]
    start = pd.to_datetime(ev["event_start"])
    end = pd.to_datetime(ev["event_end"])
    df = df.copy()
    label = ev["event_label"]
    if label == "anomaly":
        df["is_anomaly"] = ((df["time_stamp"] >= start) & (df["time_stamp"] <= end)).astype(int)
    else:
        df["is_anomaly"] = 0
    df["event_label"] = label
    return df


def zscore_detect(
    df: pd.DataFrame,
    feature_cols: List[str],
    threshold: float = 3.0,
    train_mask: Optional[pd.Series] = None,
) -> pd.DataFrame:
    """Flag rows where any feature z-score exceeds threshold.

    Stats are computed on the training portion (train_mask True) and applied
    to the whole frame.
    """
    if train_mask is None:
        train_mask = df["train_test"] == "train" if "train_test" in df.columns else pd.Series(True, index=df.index)
    train = df.loc[train_mask, feature_cols]
    means = train.mean()
    stds = train.std().replace(0, np.nan)
    z = (df[feature_cols] - means) / stds
    df = df.copy()
    df["anomaly_score"] = z.abs().max(axis=1)
    df["is_pred_anomaly"] = (df["anomaly_score"] > threshold).astype(int)
    return df


def evaluate(y_true: np.ndarray, y_pred: np.ndarray, timestamps: Optional[pd.Series] = None) -> Dict:
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    out = {
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "n_true": int(y_true.sum()),
        "n_pred": int(y_pred.sum()),
        "n_total": int(len(y_true)),
    }
    if timestamps is not None:
        ts = pd.to_datetime(timestamps)
        # false alarms per day on the whole window
        days = (ts.max() - ts.min()).total_seconds() / 86400.0
        fp = int(((y_true == 0) & (y_pred == 1)).sum())
        out["false_alarms_per_day"] = float(fp / days) if days > 0 else float("nan")
        # detection lead time: first alarm before/at event start
        true_idx = np.where(y_true == 1)[0]
        if len(true_idx):
            event_start = ts.iloc[true_idx[0]]
            alarm_idx = np.where(y_pred == 1)[0]
            if len(alarm_idx):
                first_alarm = ts.iloc[alarm_idx[0]]
                out["first_alarm"] = str(first_alarm)
                out["detection_lead_time_min"] = float((event_start - first_alarm).total_seconds() / 60.0)
    return out

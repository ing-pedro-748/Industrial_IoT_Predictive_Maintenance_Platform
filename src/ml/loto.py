"""Leave-One-Turbine-Out (LOTO) evaluation."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from src.utils.data_loader import DatasetSource
from src.ml.baseline import add_event_labels, evaluate
from src.ml.isolation_forest import train_iforest, predict_iforest


def load_farm_series(source: DatasetSource, farm: str, event_info: pd.DataFrame) -> pd.DataFrame:
    """Load all datasets for a farm, tag with turbine (asset_id) and event metadata."""
    frames = []
    for _, ev in event_info.iterrows():
        eid = int(ev["event_id"])
        asset = int(ev["asset"] if "asset" in ev else ev["asset_id"])
        rel = f"Wind Farm {farm}/datasets/{eid}.csv"
        df = source.read_csv(rel, sep=";")
        df["time_stamp"] = pd.to_datetime(df["time_stamp"])
        df["event_id"] = eid
        df["asset_id"] = asset
        df["event_label"] = ev["event_label"]
        # event interval
        start = pd.to_datetime(ev["event_start"])
        end = pd.to_datetime(ev["event_end"])
        if ev["event_label"] == "anomaly":
            df["is_anomaly"] = ((df["time_stamp"] >= start) & (df["time_stamp"] <= end)).astype(int)
        else:
            df["is_anomaly"] = 0
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def zscore_fit(train_df: pd.DataFrame, feature_cols: List[str]) -> tuple:
    means = train_df[feature_cols].mean()
    stds = train_df[feature_cols].std().replace(0, np.nan)
    return means, stds


def zscore_predict(df: pd.DataFrame, means, stds, feature_cols: List[str], threshold: float) -> pd.DataFrame:
    z = (df[feature_cols] - means) / stds
    df = df.copy()
    df["anomaly_score"] = z.abs().max(axis=1)
    df["is_pred_anomaly"] = (df["anomaly_score"] > threshold).astype(int)
    return df


def event_detection_rate(pred_df: pd.DataFrame, event_info: pd.DataFrame) -> Dict:
    """Fraction of anomaly events with at least one alarm in their interval."""
    events = event_info[event_info["event_label"] == "anomaly"]
    detected = 0
    lead_times = []
    for _, ev in events.iterrows():
        eid = int(ev["event_id"])
        start = pd.to_datetime(ev["event_start"])
        end = pd.to_datetime(ev["event_end"])
        sub = pred_df[(pred_df["event_id"] == eid) & (pred_df["train_test"] == "prediction")]
        alarms = sub[(sub["is_pred_anomaly"] == 1) & (sub["time_stamp"] >= start) & (sub["time_stamp"] <= end)]
        if len(alarms) > 0:
            detected += 1
            first = alarms["time_stamp"].min()
            lead_times.append((start - first).total_seconds() / 60.0)
    rate = detected / len(events) if len(events) else float("nan")
    avg_lead = float(np.mean(lead_times)) if lead_times else float("nan")
    return {"event_detection_rate": rate, "n_events": len(events), "n_detected": detected, "avg_lead_time_min": avg_lead}


def loto_fold(
    all_df: pd.DataFrame,
    feature_cols: List[str],
    test_asset: int,
    event_info: pd.DataFrame,
    models: List[str],
    if_contaminations: List[float] = (0.05, 0.10, 0.15),
    z_threshold: float = 2.0,
) -> List[Dict]:
    train_df = all_df[all_df["asset_id"] != test_asset]
    test_df = all_df[all_df["asset_id"] == test_asset]

    train_mask = train_df["train_test"] == "train"
    train_data = train_df[train_mask]

    results = []

    # Z-score
    if "zscore" in models:
        means, stds = zscore_fit(train_data, feature_cols)
        test_pred = zscore_predict(test_df, means, stds, feature_cols, z_threshold)
        pred = test_pred[test_pred["train_test"] == "prediction"]
        m = evaluate(pred["is_anomaly"].values, pred["is_pred_anomaly"].values, pred["time_stamp"])
        # filter event_info to test asset
        asset_col = "asset" if "asset" in event_info.columns else "asset_id"
        ei_test = event_info[event_info[asset_col] == test_asset]
        m.update(event_detection_rate(pred, ei_test))
        m["model"] = "zscore"
        m["test_asset"] = test_asset
        m["contamination"] = None
        m["threshold"] = z_threshold
        results.append(m)

    # Isolation Forest
    for cont in if_contaminations:
        if "iforest" in models:
            model = train_iforest(train_data, feature_cols, contamination=cont)
            test_pred = predict_iforest(test_df, model, feature_cols)
            pred = test_pred[test_pred["train_test"] == "prediction"]
            m = evaluate(pred["is_anomaly"].values, pred["is_pred_anomaly"].values, pred["time_stamp"])
            asset_col = "asset" if "asset" in event_info.columns else "asset_id"
            ei_test = event_info[event_info[asset_col] == test_asset]
            m.update(event_detection_rate(pred, ei_test))
            m["model"] = "iforest"
            m["test_asset"] = test_asset
            m["contamination"] = cont
            m["threshold"] = None
            results.append(m)

    return results


def run_loto(
    source: DatasetSource,
    farm: str,
    feature_cols: List[str],
    event_info: pd.DataFrame,
    models: List[str] = ("zscore", "iforest"),
    if_contaminations: List[float] = (0.05, 0.10, 0.15),
    z_threshold: float = 2.0,
) -> pd.DataFrame:
    all_df = load_farm_series(source, farm, event_info)
    asset_col = "asset" if "asset" in event_info.columns else "asset_id"
    assets = sorted(event_info[asset_col].unique())
    all_results = []
    for asset in assets:
        print(f"Fold test_asset={asset}")
        res = loto_fold(all_df, feature_cols, int(asset), event_info, list(models), list(if_contaminations), z_threshold)
        all_results.extend(res)
    return pd.DataFrame(all_results)

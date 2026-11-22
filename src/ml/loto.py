"""Leave-One-Turbine-Out (LOTO) evaluation."""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from src.utils.data_loader import DatasetSource
from src.ml.baseline import evaluate
from src.ml.isolation_forest import train_iforest, predict_iforest
from src.features.rolling import add_rolling_features, rolling_feature_names


def load_farm_series(source: DatasetSource, farm: str, event_info: pd.DataFrame) -> pd.DataFrame:
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
        start = pd.to_datetime(ev["event_start"])
        end = pd.to_datetime(ev["event_end"])
        if ev["event_label"] == "anomaly":
            df["is_anomaly"] = ((df["time_stamp"] >= start) & (df["time_stamp"] <= end)).astype(int)
        else:
            df["is_anomaly"] = 0
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def zscore_fit(train_df, feature_cols):
    means = train_df[feature_cols].mean()
    stds = train_df[feature_cols].std().replace(0, np.nan)
    return means, stds


def zscore_predict(df, means, stds, feature_cols, threshold):
    z = (df[feature_cols] - means) / stds
    df = df.copy()
    df["anomaly_score"] = z.abs().max(axis=1)
    df["is_pred_anomaly"] = (df["anomaly_score"] > threshold).astype(int)
    return df


def event_detection_rate(pred_df, event_info):
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
            lead_times.append((start - alarms["time_stamp"].min()).total_seconds() / 60.0)
    rate = detected / len(events) if len(events) else float("nan")
    avg_lead = float(np.mean(lead_times)) if lead_times else float("nan")
    return {"event_detection_rate": rate, "n_events": len(events), "n_detected": detected, "avg_lead_time_min": avg_lead}


def calibrate_zscore(train_data, feature_cols, val_fraction=0.2, candidates=None):
    if candidates is None:
        candidates = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    # time-based split
    train_data = train_data.sort_values("time_stamp")
    cutoff = train_data["time_stamp"].quantile(1 - val_fraction)
    tr = train_data[train_data["time_stamp"] <= cutoff]
    va = train_data[train_data["time_stamp"] > cutoff]
    means, stds = zscore_fit(tr, feature_cols)
    va_pred = zscore_predict(va.copy(), means, stds, feature_cols, 0)
    best_thr, best_f1 = candidates[0], -1
    for thr in candidates:
        yp = (va_pred["anomaly_score"] > thr).astype(int)
        from sklearn.metrics import f1_score
        f1 = f1_score(va["is_anomaly"].values, yp.values, zero_division=0)
        if f1 > best_f1:
            best_f1, best_thr = f1, thr
    return best_thr, means, stds


def calibrate_iforest(train_data, feature_cols, contamination, val_fraction=0.2, candidates=None):
    if candidates is None:
        candidates = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    train_data = train_data.sort_values("time_stamp")
    cutoff = train_data["time_stamp"].quantile(1 - val_fraction)
    tr = train_data[train_data["time_stamp"] <= cutoff]
    va = train_data[train_data["time_stamp"] > cutoff]
    model = train_iforest(tr, feature_cols, contamination=contamination)
    va_pred = predict_iforest(va.copy(), model, feature_cols)
    best_thr, best_f1 = None, -1
    for thr in candidates:
        yp = (va_pred["anomaly_score"] > thr).astype(int)
        from sklearn.metrics import f1_score
        f1 = f1_score(va["is_anomaly"].values, yp.values, zero_division=0)
        if f1 > best_f1:
            best_f1, best_thr = f1, thr
    # fallback to contamination-based (no threshold) if no candidate beats
    if best_thr is None:
        best_thr = None
    return model, best_thr


def loto_fold(all_df, feature_cols, test_asset, event_info, use_rolling, windows, calibrate, z_threshold, if_contaminations):
    train_df = all_df[all_df["asset_id"] != test_asset]
    test_df = all_df[all_df["asset_id"] == test_asset]
    train_mask = train_df["train_test"] == "train"
    train_data = train_df[train_mask].copy()
    asset_col = "asset" if "asset" in event_info.columns else "asset_id"
    ei_test = event_info[event_info[asset_col] == test_asset]

    results = []

    # Z-score
    if calibrate:
        thr, means, stds = calibrate_zscore(train_data, feature_cols)
    else:
        means, stds = zscore_fit(train_data, feature_cols)
        thr = z_threshold
    test_pred = zscore_predict(test_df.copy(), means, stds, feature_cols, thr)
    pred = test_pred[test_pred["train_test"] == "prediction"]
    m = evaluate(pred["is_anomaly"].values, pred["is_pred_anomaly"].values, pred["time_stamp"])
    m.update(event_detection_rate(pred, ei_test))
    m["model"] = "zscore"
    m["test_asset"] = test_asset
    m["contamination"] = None
    m["threshold"] = thr
    m["calibrated"] = calibrate
    results.append(m)

    # Isolation Forest
    for cont in if_contaminations:
        model = train_iforest(train_data, feature_cols, contamination=cont)
        thr = None
        test_pred = predict_iforest(test_df.copy(), model, feature_cols, threshold=thr)
        pred = test_pred[test_pred["train_test"] == "prediction"]
        m = evaluate(pred["is_anomaly"].values, pred["is_pred_anomaly"].values, pred["time_stamp"])
        m.update(event_detection_rate(pred, ei_test))
        m["model"] = "iforest"
        m["test_asset"] = test_asset
        m["contamination"] = cont
        m["threshold"] = thr
        m["calibrated"] = calibrate
        results.append(m)

    return results


def run_loto(source, farm, feature_cols, event_info, use_rolling=False, windows=(6, 36), calibrate=False, if_contaminations=(0.05, 0.10, 0.15), z_threshold=2.0):
    all_df = load_farm_series(source, farm, event_info)
    if use_rolling:
        all_df = add_rolling_features(all_df, feature_cols, windows=windows)
        feature_cols = rolling_feature_names(feature_cols, windows)
    asset_col = "asset" if "asset" in event_info.columns else "asset_id"
    assets = sorted(event_info[asset_col].unique())
    all_results = []
    for asset in assets:
        print(f"Fold test_asset={asset}")
        res = loto_fold(all_df, feature_cols, int(asset), event_info, use_rolling, windows, calibrate, z_threshold, list(if_contaminations))
        all_results.extend(res)
    return pd.DataFrame(all_results)

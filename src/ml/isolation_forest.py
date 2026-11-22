"""Isolation Forest anomaly detection."""
from __future__ import annotations

from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from src.ml.baseline import evaluate


def train_iforest(
    df: pd.DataFrame,
    feature_cols: List[str],
    contamination: float = 0.05,
    train_mask: Optional[pd.Series] = None,
    random_state: int = 42,
) -> IsolationForest:
    if train_mask is None:
        train_mask = df["train_test"] == "train" if "train_test" in df.columns else pd.Series(True, index=df.index)
    X = df.loc[train_mask, feature_cols].fillna(0)
    model = IsolationForest(contamination=contamination, random_state=random_state, n_estimators=200)
    model.fit(X)
    return model


def predict_iforest(
    df: pd.DataFrame,
    model: IsolationForest,
    feature_cols: List[str],
    threshold: Optional[float] = None,
) -> pd.DataFrame:
    X = df[feature_cols].fillna(0)
    scores = -model.decision_function(X)  # higher = more anomalous
    preds = model.predict(X)  # -1 anomaly, 1 normal
    df = df.copy()
    df["anomaly_score"] = scores
    if threshold is None:
        df["is_pred_anomaly"] = (preds == -1).astype(int)
    else:
        df["is_pred_anomaly"] = (scores > threshold).astype(int)
    return df


def run_iforest_experiment(
    df: pd.DataFrame,
    feature_cols: List[str],
    contamination: float,
    threshold: Optional[float] = None,
) -> Dict:
    model = train_iforest(df, feature_cols, contamination=contamination)
    df = predict_iforest(df, model, feature_cols, threshold=threshold)
    pred = df[df["train_test"] == "prediction"]
    m = evaluate(pred["is_anomaly"].values, pred["is_pred_anomaly"].values, pred["time_stamp"])
    m["contamination"] = contamination
    m["threshold"] = threshold
    return m, df

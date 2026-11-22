"""Rolling window feature engineering (leakage-safe)."""
from __future__ import annotations

from typing import List

import pandas as pd


def add_rolling_features(
    df: pd.DataFrame,
    feature_cols: List[str],
    windows: List[int] = (6, 36),
    group_col: str = "asset_id",
    time_col: str = "time_stamp",
) -> pd.DataFrame:
    """Add rolling mean/std for each feature over given window sizes (in rows).

    Windows are applied per group (turbine) and shifted by 1 to avoid using the
    current observation (leakage-safe). Requires sorted time within group.
    """
    df = df.sort_values([group_col, time_col]).copy()
    for w in windows:
        for col in feature_cols:
            g = df.groupby(group_col)[col]
            df[f"{col}_roll{w}_mean"] = g.transform(lambda s: s.shift(1).rolling(w, min_periods=1).mean())
            df[f"{col}_roll{w}_std"] = g.transform(lambda s: s.shift(1).rolling(w, min_periods=1).std())
    return df.reset_index(drop=True)


def rolling_feature_names(feature_cols: List[str], windows: List[int] = (6, 36)) -> List[str]:
    out = list(feature_cols)
    for w in windows:
        for col in feature_cols:
            out.append(f"{col}_roll{w}_mean")
            out.append(f"{col}_roll{w}_std")
    return out

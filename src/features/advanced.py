"""Advanced feature engineering: lags, rolling min/max, differences."""
from __future__ import annotations

from typing import List

import pandas as pd


def add_lag_features(df: pd.DataFrame, feature_cols: List[str], lags: List[int] = (1, 6), group_col: str = "asset_id", time_col: str = "time_stamp") -> pd.DataFrame:
    df = df.sort_values([group_col, time_col]).copy()
    for lag in lags:
        for col in feature_cols:
            df[f"{col}_lag{lag}"] = df.groupby(group_col)[col].shift(lag)
    return df.reset_index(drop=True)


def add_rolling_minmax(df: pd.DataFrame, feature_cols: List[str], windows: List[int] = (6, 36), group_col: str = "asset_id", time_col: str = "time_stamp") -> pd.DataFrame:
    df = df.sort_values([group_col, time_col]).copy()
    for w in windows:
        for col in feature_cols:
            g = df.groupby(group_col)[col]
            df[f"{col}_roll{w}_min"] = g.transform(lambda s: s.shift(1).rolling(w, min_periods=1).min())
            df[f"{col}_roll{w}_max"] = g.transform(lambda s: s.shift(1).rolling(w, min_periods=1).max())
    return df.reset_index(drop=True)


def add_diff_features(df: pd.DataFrame, feature_cols: List[str], group_col: str = "asset_id") -> pd.DataFrame:
    df = df.copy()
    for col in feature_cols:
        df[f"{col}_diff1"] = df.groupby(group_col)[col].diff(1)
    return df

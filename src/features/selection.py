"""Feature selection helpers for CARE to Compare V6."""
from __future__ import annotations

from typing import List

import pandas as pd

from src.utils.data_loader import DatasetSource
from src.profiling.equivalence import build_equivalence_table, categorize


PRIORITY_CATEGORIES = ["temperature", "power", "wind", "pitch", "vibration", "pressure"]


def select_pilot_features(farm: str, n_per_category: int = 3) -> List[str]:
    """Select up to n_per_category sensor columns per priority category for a farm."""
    src = DatasetSource()
    fd = src.read_csv(f"Wind Farm {farm}/feature_description.csv", sep=";")
    fd = fd.copy()
    fd["category"] = fd["description"].astype(str).apply(categorize)
    chosen: List[str] = []
    for cat in PRIORITY_CATEGORIES:
        sub = fd[(fd["category"] == cat) & (fd["unit"].notna())]
        # prefer sensors that have avg statistic
        sub = sub[sub["statistics_type"].str.contains("average", case=False, na=False)]
        for _, row in sub.head(n_per_category).iterrows():
            col = f"{row['sensor_name']}_avg"
            if col not in chosen:
                chosen.append(col)
    return chosen

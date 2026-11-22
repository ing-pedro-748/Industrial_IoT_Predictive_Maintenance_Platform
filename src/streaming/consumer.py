"""Streaming consumer: process events, aggregate windows, infer anomalies."""
from __future__ import annotations

from collections import deque
from datetime import datetime, timedelta
from typing import Deque, Dict, List, Optional

import numpy as np
import pandas as pd

from src.ml.baseline import zscore_detect


class WindowAggregator:
    """Maintain a sliding window of events per turbine and compute aggregates."""

    def __init__(self, window_size: int = 6):
        self.window_size = window_size
        self.buffers: dict = {}

    def add(self, event: Dict):
        key = (event["farm"], event["asset_id"])
        self.buffers.setdefault(key, deque(maxlen=self.window_size))
        self.buffers[key].append(event)

    def aggregate(self, key) -> Optional[Dict]:
        buf = self.buffers.get(key)
        if not buf or len(buf) < 1:
            return None
        df = pd.DataFrame(list(buf))
        agg = {"farm": key[0], "asset_id": key[1], "n": len(df)}
        for col in [c for c in df.columns if c not in ("event_time", "ingestion_time", "farm", "asset_id", "status_type_id")]:
            vals = pd.to_numeric(df[col], errors="coerce")
            agg[f"{col}_mean"] = float(vals.mean()) if vals.notna().any() else None
        return agg

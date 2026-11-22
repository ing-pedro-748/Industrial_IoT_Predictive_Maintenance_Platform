"""Sensor simulator: replay SCADA series as telemetry events."""
from __future__ import annotations

import json
import time
from datetime import datetime, timedelta
from typing import Callable, Dict, Iterable, Optional

import pandas as pd


def build_event(row: pd.Series, farm: str, feature_cols: list) -> Dict:
    ev = {
        "event_time": str(row["time_stamp"]),
        "ingestion_time": datetime.utcnow().isoformat(),
        "farm": farm,
        "asset_id": int(row["asset_id"]),
        "status_type_id": int(row["status_type_id"]),
    }
    for c in feature_cols:
        ev[c] = float(row[c]) if pd.notna(row[c]) else None
    return ev


def replay_series(
    df: pd.DataFrame,
    farm: str,
    feature_cols: list,
    publish: Callable[[Dict], None],
    speed: float = 1.0,
    max_events: Optional[int] = None,
):
    """Replay a dataframe, calling publish(event) for each row."""
    df = df.sort_values("time_stamp").reset_index(drop=True)
    n = 0
    for _, row in df.iterrows():
        ev = build_event(row, farm, feature_cols)
        publish(ev)
        n += 1
        if max_events and n >= max_events:
            break
        if speed > 0:
            time.sleep(0)  # no real sleep for demo; set speed>0 to throttle
    return n

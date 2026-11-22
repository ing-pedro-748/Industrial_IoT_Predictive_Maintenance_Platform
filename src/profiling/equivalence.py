"""Build a sensor equivalence table across wind farms."""
from __future__ import annotations

import re
from typing import Dict

import pandas as pd

from src.utils.data_loader import DatasetSource


KEYWORDS = {
    "temperature": ["temp", "temperature"],
    "wind": ["wind", "windspeed", "anemometer"],
    "power": ["power", "active power", "reactive"],
    "pitch": ["pitch"],
    "vibration": ["vibr", "acceleration"],
    "pressure": ["pressure", "bar"],
    "current": ["current", "amp", " A"],
    "voltage": ["voltage", " V"],
    "rotation": ["rpm", "speed", "rotor"],
}


def categorize(description: str) -> str:
    d = (description or "").lower()
    for cat, kws in KEYWORDS.items():
        if any(kw in d for kw in kws):
            return cat
    return "other"


def build_equivalence_table(source: DatasetSource) -> pd.DataFrame:
    frames = []
    for farm in ["Wind Farm A", "Wind Farm B", "Wind Farm C"]:
        fd = source.read_csv(f"{farm}/feature_description.csv", sep=";")
        fd = fd.copy()
        fd["farm"] = farm.replace("Wind Farm ", "")
        fd["category"] = fd["description"].astype(str).apply(categorize)
        frames.append(fd)
    return pd.concat(frames, ignore_index=True)


def pilot_candidates(eq: pd.DataFrame, min_farms: int = 2) -> pd.DataFrame:
    """Sensors whose (category, unit) appears in at least min_farms farms."""
    g = eq.groupby(["category", "unit"])["farm"].nunique().reset_index(name="n_farms")
    keep = g[g["n_farms"] >= min_farms]
    merged = eq.merge(keep[["category", "unit"]], on=["category", "unit"], how="inner")
    return merged.sort_values(["category", "unit", "farm"])

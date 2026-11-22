"""Local warehouse helper using DuckDB (Snowflake alternative for MVP)."""
from __future__ import annotations

from pathlib import Path

import duckdb
import pandas as pd


def create_local_warehouse(db_path: str = "data/warehouse.duckdb"):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(db_path)
    # create tables
    con.execute("""
        CREATE TABLE IF NOT EXISTS dim_turbine (
            turbine_id INTEGER PRIMARY KEY,
            farm VARCHAR,
            asset_id INTEGER
        );
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS fact_anomaly_prediction (
            turbine_id INTEGER,
            ts TIMESTAMP,
            anomaly_score DOUBLE,
            is_anomaly BOOLEAN,
            model_version VARCHAR
        );
    """)
    con.close()
    return db_path


def load_predictions(db_path: str, df: pd.DataFrame):
    con = duckdb.connect(db_path)
    con.register("pred_df", df)
    con.execute("INSERT INTO fact_anomaly_prediction SELECT turbine_id, ts, anomaly_score, is_anomaly, model_version FROM pred_df")
    con.close()

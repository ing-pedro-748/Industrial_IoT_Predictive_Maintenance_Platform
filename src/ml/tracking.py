"""MLflow experiment tracking helpers."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict

import mlflow


def init_tracking(experiment_name: str = "industrial-iot-pm", tracking_uri: str = None):
    if tracking_uri is None:
        tracking_uri = os.environ.get("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)


def log_run(run_name: str, params: Dict[str, Any], metrics: Dict[str, float], artifact_path: str = None):
    with mlflow.start_run(run_name=run_name):
        for k, v in params.items():
            mlflow.log_param(k, v)
        for k, v in metrics.items():
            if v is not None and not (isinstance(v, float) and (v != v)):  # skip nan
                mlflow.log_metric(k, float(v))
        if artifact_path and Path(artifact_path).exists():
            mlflow.log_artifact(artifact_path)

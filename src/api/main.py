"""FastAPI inference service for the predictive maintenance model."""
from __future__ import annotations

import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

MODEL_PATH = ROOT / "models" / "if_a.pkl"

app = FastAPI(title="Industrial IoT PM - Anomaly Detection")

_model_bundle = None


def load_model():
    global _model_bundle
    if _model_bundle is None:
        _model_bundle = joblib.load(MODEL_PATH)
    return _model_bundle


class PredictRequest(BaseModel):
    features: list[float]


class PredictResponse(BaseModel):
    anomaly_score: float
    is_anomaly: bool
    model_version: str = "if_farmA_v1"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    bundle = load_model()
    model = bundle["model"]
    features = bundle["features"]
    x = np.array(req.features, dtype=float).reshape(1, -1)
    x_df = pd.DataFrame(x, columns=features)
    score = float(-model.decision_function(x_df)[0])
    pred = int(model.predict(x_df)[0] == -1)
    return PredictResponse(anomaly_score=score, is_anomaly=bool(pred))

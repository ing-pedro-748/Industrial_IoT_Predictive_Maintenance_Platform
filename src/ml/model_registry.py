"""Train and register a final model in MLflow."""
from __future__ import annotations

import sys
from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from src.features.pilot_sets import PILOT_FEATURES
from src.features.rolling import add_rolling_features, rolling_feature_names
from src.utils.data_loader import DatasetSource
from src.ml.tracking import init_tracking


def train_final_model(farm: str = "A", contamination: float = 0.15):
    src = DatasetSource()
    ei = src.read_csv(f"Wind Farm {farm}/event_info.csv", sep=";")
    feats = PILOT_FEATURES[farm]
    # load all train portions
    frames = []
    for _, ev in ei.iterrows():
        eid = int(ev["event_id"])
        asset = int(ev["asset"] if "asset" in ev else ev["asset_id"])
        rel = f"Wind Farm {farm}/datasets/{eid}.csv"
        df = src.read_csv(rel, sep=";")
        df = df[df["asset_id"] == asset]
        df = df[df["train_test"] == "train"]
        frames.append(df)
    train_df = pd.concat(frames, ignore_index=True)
    train_df = add_rolling_features(train_df, feats, windows=(6, 36))
    all_feats = rolling_feature_names(feats, (6, 36))
    X = train_df[all_feats].fillna(0)
    model = IsolationForest(contamination=contamination, random_state=42, n_estimators=200)
    model.fit(X)

    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    model_path = models_dir / f"if_{farm.lower()}.pkl"
    joblib.dump({"model": model, "features": all_feats, "farm": farm}, model_path)

    init_tracking("industrial-iot-pm")
    with mlflow.start_run(run_name=f"final_model_farm{farm}"):
        mlflow.log_param("farm", farm)
        mlflow.log_param("contamination", contamination)
        mlflow.log_param("n_features", len(all_feats))
        mlflow.sklearn.log_model(model, artifact_path="model", registered_model_name=f"if_farm{farm}",
                                skops_trusted_types=["sklearn.tree._tree.Tree"])
    print("registered", model_path)
    return model_path


if __name__ == "__main__":
    train_final_model("A", 0.15)

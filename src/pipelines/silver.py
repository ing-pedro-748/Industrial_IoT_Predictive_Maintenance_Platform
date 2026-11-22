"""Silver layer: validate, type, clean raw bronze data."""
from __future__ import annotations

from pathlib import Path

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F


def silver_transform(bronze_path: str, output_base: str, farm: str) -> str:
    spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    df = spark.read.parquet(bronze_path)
    # parse timestamp
    df = df.withColumn("time_stamp", F.to_timestamp(F.col("time_stamp")))
    # cast numeric sensor columns
    for c in df.columns:
        if c not in ("time_stamp", "asset_id", "id", "train_test", "status_type_id"):
            df = df.withColumn(c, F.col(c).cast("double"))
    out = Path(output_base) / "silver" / farm.replace(" ", "_")
    out.mkdir(parents=True, exist_ok=True)
    df.write.mode("overwrite").partitionBy("asset_id").parquet(str(out))
    return str(out)

"""Gold layer: aggregated features for analytics/ML."""
from __future__ import annotations

from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def gold_aggregate(silver_path: str, output_base: str, farm: str) -> str:
    spark = SparkSession.getActiveSession() or SparkSession.builder.getOrCreate()
    df = spark.read.parquet(silver_path)
    # daily aggregates per turbine
    df = df.withColumn("date", F.to_date(F.col("time_stamp")))
    agg = df.groupBy("asset_id", "date").agg(
        F.count("*").alias("n_records"),
        F.avg("status_type_id").alias("avg_status"),
    )
    out = Path(output_base) / "gold" / farm.replace(" ", "_")
    out.mkdir(parents=True, exist_ok=True)
    agg.write.mode("overwrite").parquet(str(out))
    return str(out)

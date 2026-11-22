"""Bronze layer: ingest raw CSVs into Parquet (Medallion)."""
from __future__ import annotations

import os
from pathlib import Path

from pyspark.sql import SparkSession


def get_spark(app_name: str = "iot-pm-bronze") -> SparkSession:
    return (
        SparkSession.builder.appName(app_name)
        .master("local[*]")
        .config("spark.driver.memory", "4g")
        .config("spark.executor.memory", "4g")
        .config("spark.sql.parquet.compression.codec", "snappy")
        .getOrCreate()
    )


def bronze_ingest_farm(spark: SparkSession, source_csv_dir: str, farm: str, output_base: str) -> str:
    """Read raw CSVs for a farm via Spark native reader and write as Parquet."""
    src = Path(source_csv_dir) / farm / "datasets"
    out = Path(output_base) / "bronze" / farm.replace(" ", "_")
    out.mkdir(parents=True, exist_ok=True)
    df = spark.read.option("header", True).option("sep", ";").csv(str(src))
    df.write.mode("overwrite").partitionBy("asset_id").parquet(str(out))
    return str(out)

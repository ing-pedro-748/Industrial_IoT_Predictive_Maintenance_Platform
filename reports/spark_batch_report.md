# Phase 3 — Spark Batch / Data Lake Report

## Pipeline implemented
- Bronze: raw CSVs → Parquet, partitioned by asset_id.
- Silver: timestamp parsing, numeric casting, schema validation.
- Gold: daily aggregates per turbine (n_records, avg_status).

## Results (Farm A)
- Bronze rows: 1,196,747
- Silver rows: 1,196,747
- Gold rows: 2,976 (daily per turbine)

## Storage
- Local filesystem as Data Lake (data/lake/). S3-compatible; swap path for S3 URI.
- Format: Parquet (snappy).

## Environment notes
- Requires Java 17+ and Hadoop winutils on Windows (set JAVA_HOME, HADOOP_HOME).
- PYSPARK_PYTHON must point to the venv python.
- In production (AWS EMR), native Hadoop is available.

## Next steps
- Extend to Farms B/C.
- Add data quality checks (null rates, schema validation) in Silver.
- Add feature engineering in Gold (rolling features via Spark).
- Phase 4: streaming pipeline.

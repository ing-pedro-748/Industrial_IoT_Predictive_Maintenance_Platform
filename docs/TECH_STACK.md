# Tech Stack

## Confirmed
- Python, Pandas, NumPy, Matplotlib, PyArrow
- Scikit-learn (baseline ML)
- Apache Kafka (streaming ingestion)
- Apache Spark / Structured Streaming
- AWS S3 (data lake) — local alternative: MinIO or local filesystem
- Snowflake (warehouse) — local alternative: PostgreSQL/DuckDB
- Apache Airflow (orchestration)
- MLflow (tracking/registry)
- FastAPI (inference)
- Power BI (visualization)
- Docker, GitHub Actions, Terraform

## Provisional
- Evidently AI (monitoring) — evaluate need
- AWS SageMaker (managed hosting) — evaluate cost/benefit
- AWS ECS Fargate (API hosting) — evaluate

## Optional (only if justified)
- AWS MSK, Glue, EMR Serverless, MWAA

## Local-first strategy
Cloud services requiring payment are optional. We will first run locally with
Docker Compose and provide local alternatives (MinIO, PostgreSQL/DuckDB) so the
platform can be demonstrated without cloud costs.

# Roadmap

## Phase 0 — Dataset Exploration and Audit (COMPLETED)
- Notebook + audit report created.

## Phase 1 — Data Understanding and Preparation (IN PROGRESS)
- Data dictionary, canonical schema, validation rules created.
- Variable equivalence analysis (preliminary).
- Missing values and temporal splits strategy documented.
- Next: build per-sensor equivalence table, profile all files, define cutoffs.

## Phase 2 — Machine Learning and Anomaly Detection (IN PROGRESS)
- Statistical baseline (Z-score) and Isolation Forest implemented.
- LOTO evaluation (raw + rolling features) across Farms A/B/C.
- Refined feature sets per farm.
- Threshold calibration (F1 and cost-aware).
- Cross-farm summary report.
- Next: MLflow tracking (Phase 6) and further feature engineering.

## Phase 3 — Data Engineering and Data Lake
- Spark batch pipelines, schema validation, Medallion layers, Parquet, partitioning, DQ checks.

## Phase 4 — IoT Streaming Pipeline
- Python sensor simulator, Kafka, Spark Structured Streaming, windows, late data, checkpoints, inference integration.

## Phase 5 — Orchestration and Data Warehouse
- Airflow DAGs, Snowflake model (facts/dimensions), data marts, SQL KPIs.

## Phase 6 — MLOps and Model Serving (IN PROGRESS)
- MLflow tracking integrated (sqlite backend).
- Experiment logging for LOTO results across farms.
- Next: model registry, FastAPI serving, prediction logging.

## Phase 7 — Analytics and Dashboard
- Power BI dashboards connected to Snowflake.

## Phase 8 — Cloud Deployment and DevOps
- Terraform, Docker, GitHub Actions, AWS services (S3, IAM, CloudWatch, ECR, ECS, optional SageMaker).

## Dependencies
Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5 -> Phase 6 -> Phase 7 -> Phase 8.
Phase 3 and 4 can partially overlap after Phase 2 model baseline.

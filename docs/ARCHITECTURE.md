# Architecture

## 1. High-level architecture

Four domains: Data Ingestion, Data Processing & Storage, ML & MLOps,
Data Consumption & Visualization.

```mermaid
flowchart LR
    A[CARE to Compare V6] --> B[Python/Pandas]
    B --> C[Data Validation]
    C --> D[Spark Batch]
    D --> E[Feature Engineering]
    E --> F[S3 Data Lake\nBronze/Silver/Gold]
    F --> G[ML Training\nScikit-learn]
    F --> H[Snowflake DW]
    G --> I[MLflow Registry]
    I --> J[FastAPI Inference]
    J --> K[Kafka prediction-results]
    K --> F
    K --> H
    H --> L[Power BI]
```

## 2. Streaming flow

```mermaid
flowchart LR
    A[Sensor Simulator\nPython] --> B[Kafka\nsensor-telemetry]
    B --> C[Spark Structured Streaming]
    C --> D[Window Aggregations]
    D --> E[Feature Engineering]
    E --> F[FastAPI / Model]
    F --> G[Anomaly Score]
    G --> H[Kafka\nprediction-results]
    H --> I[S3 + Snowflake]
    I --> J[Power BI]
```

## 3. Component responsibilities

| Component | Responsibility |
|---|---|
| Kafka | Event ingestion and transport |
| Spark | Data processing (batch + streaming) |
| Airflow | Workflow orchestration |
| S3 | Data lake storage (Medallion) |
| Snowflake | Analytics / data warehouse |
| MLflow | Experiment tracking & model registry |
| FastAPI | Inference service |
| Power BI | Visualization |

## 4. Data lake (Medallion)

- **Bronze**: raw events, minimal transformation.
- **Silver**: validated, cleaned, structured.
- **Gold**: aggregated, analytics/ML-ready (Parquet, partitioned).

## 5. Principles

- Separation of responsibilities.
- Incremental development (local first, cloud later).
- Reproducibility.
- Data quality first.
- No data leakage.
- Security (no secrets in repo).
- Observability.
- Documentation.

## 6. Decisions status

- **Confirmed**: Medallion on S3, FastAPI for inference, MLflow for tracking, Power BI for viz.
- **Provisional**: SageMaker/ECS hosting (evaluate later), Evidently for monitoring.
- **Pending**: per-farm schema equivalence, gap handling policy, labeling rule for evaluation.

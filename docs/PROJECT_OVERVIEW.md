# Project Overview

## 1. Project name

**Industrial IoT Predictive Maintenance Platform**

## 2. Problem statement

Industrial assets such as wind turbines generate large volumes of SCADA telemetry.
Unexpected failures lead to downtime, high maintenance costs and safety risks.
Predictive maintenance aims to detect abnormal behavior before a failure occurs,
so maintenance teams can act proactively.

## 3. Goal

Build an end-to-end platform that ingests real wind-turbine SCADA data, detects
anomalies in operational behavior, stores and serves the results, and presents
them through analytics. The platform should be reproducible, documented and
deployable, and demonstrate skills in Data Engineering, ML, MLOps and Cloud.

## 4. Machine Learning scope

- Primary task: **Anomaly Detection**.
- Strategy: learn normal behavior, flag deviations.
- Labels and documented event intervals are used for **evaluation only**, never
  as predictive features (no data leakage).
- Distinguish anomaly / failure / maintenance / alert.

## 5. Data source

- CARE to Compare V6 (Zenodo): real wind-turbine SCADA.
- Local audit results (Phase 0) are the source of truth:
  95 datasets, 3 wind farms, 36 turbines, ~5.24M rows, 10-min frequency,
  45 anomaly + 50 normal events.

## 6. Scope boundaries (current phase)

- No model training yet.
- No Kafka/Spark/Airflow/cloud services implemented yet.
- Focus: documentation, architecture, roadmap, and preparation.

## 7. Expected final capabilities

Historical batch processing, simulated streaming, anomaly inference, data lake,
data warehouse, dashboards, experiment tracking, model serving, orchestration,
and (optionally) cloud deployment.

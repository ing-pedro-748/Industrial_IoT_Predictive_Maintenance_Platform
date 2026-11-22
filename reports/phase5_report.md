# Phase 5 — Orchestration and Data Warehouse Report

## Components
- Airflow DAGs: `dags/iot_pm_batch.py` (daily batch), `dags/iot_pm_training.py` (weekly training).
- Snowflake DDL: `sql/snowflake/ddl.sql` (dim_turbine, dim_date, fact_sensor_reading, fact_anomaly_prediction, fact_event).
- KPI queries: `sql/snowflake/kpi_queries.sql`.
- Local warehouse helper: `src/warehouse/local.py` (DuckDB alternative).

## Notes
- Airflow/Snowflake not installed locally; DAGs are code artifacts for deployment.
- DuckDB used as local alternative for KPI prototyping.
- S3/Snowflake paths are configurable; local-first approach documented.

## Next steps
- Phase 6 completion: model registry + FastAPI (already started).
- Phase 7: Power BI dashboards.
- Phase 8: cloud deployment.

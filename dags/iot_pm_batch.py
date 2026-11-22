"""Airflow DAG for batch data processing."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "iot-pm",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="iot_pm_batch_pipeline",
    default_args=default_args,
    description="Batch processing of CARE to Compare V6",
    schedule_interval="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    def extract():
        print("Extract raw data")

    def transform():
        print("Spark batch transform")

    def load():
        print("Load to warehouse")

    t1 = PythonOperator(task_id="extract", python_callable=extract)
    t2 = PythonOperator(task_id="transform", python_callable=transform)
    t3 = PythonOperator(task_id="load", python_callable=load)

    t1 >> t2 >> t3
"
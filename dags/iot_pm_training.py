"""Airflow DAG for model training and evaluation."""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {"owner": "iot-pm", "retries": 1, "retry_delay": timedelta(minutes=10)}

with DAG(
    dag_id="iot_pm_training",
    default_args=default_args,
    description="Train and evaluate anomaly detection models",
    schedule_interval="@weekly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    def train():
        print("Train models")

    def evaluate():
        print("Evaluate models")

    def register():
        print("Register best model in MLflow")

    t1 = PythonOperator(task_id="train", python_callable=train)
    t2 = PythonOperator(task_id="evaluate", python_callable=evaluate)
    t3 = PythonOperator(task_id="register", python_callable=register)

    t1 >> t2 >> t3
"
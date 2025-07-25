from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def receive_trigger():
    print("Child DAG triggered successfully!")

with DAG(
    dag_id='trigger_child_dag',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    task = PythonOperator(
        task_id='print_trigger',
        python_callable=receive_trigger
    )

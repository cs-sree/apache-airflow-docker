from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

with DAG(
    dag_id='trigger_parent_dag',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    def return_one():
        return 1

    def return_two():
        return 2

    task_a = PythonOperator(task_id='task_a', python_callable=return_one)
    task_b = PythonOperator(task_id='task_b', python_callable=return_two)

    trigger = TriggerDagRunOperator(
        task_id='trigger_child',
        trigger_dag_id='trigger_child_dag'  # must match the other DAG ID
    )

    [task_a, task_b] >> trigger

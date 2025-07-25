from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.latest_only import LatestOnlyOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

with DAG(
    dag_id='latest_only_example',
    start_date=datetime(2024, 1, 1),
    schedule="@daily",  # set to test latest run effect
    catchup=True
) as dag:

    def return_one():
        return 1

    def return_two():
        return 2

    def sum_values(ti):
        a = ti.xcom_pull(task_ids='task_a')
        b = ti.xcom_pull(task_ids='task_b')
        print(f"Sum is: {a + b}")

    task_a = PythonOperator(task_id='task_a', python_callable=return_one)
    task_b = PythonOperator(task_id='task_b', python_callable=return_two)

    latest_only = LatestOnlyOperator(task_id='latest_only')

    task_sum = PythonOperator(task_id='task_sum', python_callable=sum_values)

    end = EmptyOperator(task_id='end')

    [task_a, task_b] >> latest_only >> task_sum >> end

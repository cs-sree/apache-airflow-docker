from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

with DAG(
    dag_id='branch_sum_with_block',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    def return_one():
        return 1

    def return_two():
        return 2

    def decide_path(ti):
        a = ti.xcom_pull(task_ids='task_a')
        b = ti.xcom_pull(task_ids='task_b')
        return 'task_sum' if a is not None and b is not None else 'skip_task'

    task_a = PythonOperator(task_id='task_a', python_callable=return_one)
    task_b = PythonOperator(task_id='task_b', python_callable=return_two)

    branch = BranchPythonOperator(task_id='branch_task', python_callable=decide_path)

    def sum_values(ti):
        a = ti.xcom_pull(task_ids='task_a')
        b = ti.xcom_pull(task_ids='task_b')
        print(f"Sum is: {a + b}")

    task_sum = PythonOperator(task_id='task_sum', python_callable=sum_values)
    skip_task = EmptyOperator(task_id='skip_task')
    end = EmptyOperator(task_id='end')

    # Set dependencies
    [task_a, task_b] >> branch
    branch >> [task_sum, skip_task] >> end

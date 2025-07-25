from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2024, 1, 1),
    'retries': 0
}

with DAG(
    dag_id='python_operator_sum_example',
    default_args=default_args,
    schedule=None,
    catchup=False,
    description="A DAG to sum two returned values using PythonOperator",
) as dag:

    # Task A: return 1
    def return_one():
        return 1

    task_a = PythonOperator(
        task_id='task_a',
        python_callable=return_one
    )

    # Task B: return 2
    def return_two():
        return 2

    task_b = PythonOperator(
        task_id='task_b',
        python_callable=return_two
    )

    # Task C: sum values returned by A and B
    def sum_values(ti):  # `ti` = task instance context
        a = ti.xcom_pull(task_ids='task_a')
        b = ti.xcom_pull(task_ids='task_b')
        total = a + b
        print(f"Sum of A and B: {a} + {b} = {total}")
        return total

    task_sum = PythonOperator(
        task_id='task_sum',
        python_callable=sum_values
    )

    # Set task dependencies
    [task_a, task_b] >> task_sum

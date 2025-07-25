from airflow.decorators import dag, task
from airflow.operators.python import BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

@dag(
    dag_id='branch_sum_decorator_style',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
)
def branch_sum_dag():

    @task
    def task_a():
        return 1

    @task
    def task_b():
        return 2

    def decide(ti):
        a = ti.xcom_pull(task_ids='task_a')
        b = ti.xcom_pull(task_ids='task_b')
        return 'task_sum' if a and b else 'skip_task'

    branch = BranchPythonOperator(task_id='branch_task', python_callable=decide)

    @task
    def task_sum(ti):
        a = ti.xcom_pull(task_ids='task_a')
        b = ti.xcom_pull(task_ids='task_b')
        print(f"Sum is {a + b}")

    skip_task = EmptyOperator(task_id='skip_task')
    end = EmptyOperator(task_id='end')

    # DAG flow
    a = task_a()
    b = task_b()
    branch >> [task_sum(), skip_task] >> end
    [a, b] >> branch

branch_sum_dag = branch_sum_dag()

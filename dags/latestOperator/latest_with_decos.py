from airflow.decorators import dag, task
from airflow.operators.latest_only import LatestOnlyOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

@dag(
    dag_id='latest_only_decorator',
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=True
)
def latest_only_dag():

    @task
    def task_a():
        return 1

    @task
    def task_b():
        return 2

    @task
    def task_sum(a, b):
        print(f"Sum is: {a + b}")

    latest_only = LatestOnlyOperator(task_id='latest_only')
    end = EmptyOperator(task_id='end')

    a = task_a()
    b = task_b()

    result = task_sum(a, b)

    latest_only >> result >> end

latest_only_decorator_dag = latest_only_dag()

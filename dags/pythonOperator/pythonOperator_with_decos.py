from airflow.decorators import dag, task
from datetime import datetime

# Define the DAG using the decorator
@dag(
    dag_id="python_decorator_sum_example",
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    description="DAG using @dag and @task to sum two values"
)
def sum_dag():

    # Task A: returns 1
    @task
    def task_a():
        return 1

    # Task B: returns 2
    @task
    def task_b():
        return 2

    # Task C: sums A and B
    @task
    def task_sum(a: int, b: int):
        total = a + b
        print(f"Sum of A + B = {a} + {b} = {total}")
        return total

    # Define task execution flow
    a = task_a()
    b = task_b()
    task_sum(a, b)

# Instantiate the DAG
sum_dag = sum_dag()

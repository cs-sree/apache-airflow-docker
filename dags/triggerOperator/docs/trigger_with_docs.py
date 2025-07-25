from airflow.decorators import dag, task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

@dag(
    dag_id='trigger_parent_decorator',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
)
def trigger_parent():

    @task
    def task_a():
        return 1

    @task
    def task_b():
        return 2

    trigger = TriggerDagRunOperator(
        task_id='trigger_child',
        trigger_dag_id='trigger_child_dag'
    )

    a = task_a()
    b = task_b()
    [a, b] >> trigger

trigger_parent_dag = trigger_parent()

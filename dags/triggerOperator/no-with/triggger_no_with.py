from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from datetime import datetime

dag = DAG(
    dag_id='trigger_parent_dag_no_with',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
)

def return_one():
    return 1

def return_two():
    return 2

task_a = PythonOperator(task_id='task_a', python_callable=return_one, dag=dag)
task_b = PythonOperator(task_id='task_b', python_callable=return_two, dag=dag)

trigger = TriggerDagRunOperator(
    task_id='trigger_child',
    trigger_dag_id='trigger_child_dag',
    dag=dag
)

task_a >> trigger
task_b >> trigger

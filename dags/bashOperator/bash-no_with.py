from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

dag = DAG(
    dag_id='bash_sum_no_with_block',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
)

task_a = BashOperator(
    task_id='task_a',
    bash_command='echo 1 > /tmp/task_a.txt',
    dag=dag
)

task_b = BashOperator(
    task_id='task_b',
    bash_command='echo 2 > /tmp/task_b.txt',
    dag=dag
)

task_sum = BashOperator(
    task_id='task_sum',
    bash_command='a=$(cat /tmp/task_a.txt); b=$(cat /tmp/task_b.txt); echo "$a + $b = $(($a + $b))"',
    dag=dag
)

task_a >> task_sum
task_b >> task_sum

from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from datetime import datetime

@dag(
    dag_id='bash_sum_decorator_style',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False
)
def bash_sum_dag():

    task_a = BashOperator(
        task_id='task_a',
        bash_command='echo 1 > /tmp/task_a.txt'
    )

    task_b = BashOperator(
        task_id='task_b',
        bash_command='echo 2 > /tmp/task_b.txt'
    )

    task_sum = BashOperator(
        task_id='task_sum',
        bash_command='a=$(cat /tmp/task_a.txt); b=$(cat /tmp/task_b.txt); echo "$a + $b = $(($a + $b))"'
    )

    task_a >> task_sum
    task_b >> task_sum

bash_sum_dag = bash_sum_dag()

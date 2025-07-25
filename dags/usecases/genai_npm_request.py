# This code is part of an Airflow DAG that runs a Node.js npm command on the local machine
# where the necessary modules are installed. It sets up the environment and executes the npm command.
# The DAG is designed to be run in a Docker container with the required dependencies.
# Ensure that Node.js and npm are installed in the Docker image.
# The DAG is defined using the Airflow BashOperator to execute shell commands.

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

dag = DAG(
    dag_id="node_job_with_bash_operator_local",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    description="Run npm command on local machine where modules are installed",
    tags=["usageJobs", "bash", "npm"]
)

run_npm_job_local = BashOperator(
    task_id="run_genai_local",
    bash_command="""
    cd /app/analytics-data-sync && 
    npm run genai-request-usage
    """,
    dag=dag
)

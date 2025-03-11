# File: dags/airflow_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Import the main function from the main script
from main.main_script import main_function  # Import function from the main script

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'main_function_dag',
    default_args=default_args,
    description='A simple DAG to run the main function',
    schedule_interval=None,  # Set to None for manual execution
    start_date=datetime(2025, 3, 12),
    catchup=False,
)

# Create a task to call the main_function
main_task = PythonOperator(
    task_id='run_main_function',
    python_callable=main_function,  # Call the imported main function
    dag=dag,
)


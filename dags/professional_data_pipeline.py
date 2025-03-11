from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

from ELT_professional_data import extract_load,transform


default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 3, 10),
    'retries': 1,
}

dag = DAG(
    'professional_data_pipeline',
    default_args=default_args,
    schedule_interval=None,  # Set to a cron expression or None if you want to trigger manually
    catchup=False,
    description='DAG to load nested json professionals data in from local folder, flatten it and load it in postgres db',
)

# Create a task to call the main_function
extract_load_task = PythonOperator(
    task_id='extract_load_task',
    python_callable=extract_load,  # Call the imported main function
    dag=dag,
)


transform_task = PythonOperator(
    task_id='transform_task',
    python_callable=transform,  # Call the imported main function
    dag=dag,
)

extract_load_task >> transform_task
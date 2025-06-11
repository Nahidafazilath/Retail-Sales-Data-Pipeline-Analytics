from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import os

# Define environment variables for scripts
os.environ['PG_HOST'] = 'postgres' # This is the service name in docker-compose
os.environ['PG_DB'] = 'retail_db'
os.environ['PG_USER'] = 'user'
os.environ['PG_PASSWORD'] = 'password'

def get_latest_sales_file(**kwargs):
    """
    Finds the latest generated sales CSV file in the data/raw directory.
    """
    data_dir = '/opt/airflow/data/raw' # Path inside the Airflow container
    list_of_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.startswith('sales_data_') and f.endswith('.csv')]
    if not list_of_files:
        # If no files, return None or raise an exception as per desired behavior
        print("No sales data CSV files found in data/raw. This might be expected on first run or if data generation failed.")
        kwargs['ti'].xcom_push(key='latest_sales_file', value=None)
        return # Exit the function cleanly
    latest_file = max(list_of_files, key=os.path.getctime)
    kwargs['ti'].xcom_push(key='latest_sales_file', value=latest_file)
    print(f"Latest sales file found: {latest_file}")


with DAG(
    dag_id='retail_sales_pipeline',
    start_date=days_ago(1),
    schedule_interval='@daily', # Run once a day
    catchup=False,
    tags=['retail', 'sales', 'data_engineering'],
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    }
) as dag:
    # Task 1: Generate daily simulated sales data
    generate_sales_data = BashOperator(
        task_id='generate_daily_sales_data',
        bash_command='python /opt/airflow/scripts/generate_sales_data.py',
    )

    # Task 2: Get the path of the newly generated sales data file
    get_latest_sales_file_path = PythonOperator(
        task_id='get_latest_sales_file_path',
        python_callable=get_latest_sales_file,
    )

    # Task 3: Ingest raw sales data into PostgreSQL
    ingest_raw_data = BashOperator(
        task_id='ingest_raw_sales_to_postgres',
        bash_command='python /opt/airflow/scripts/ingest_data_to_postgres.py {{ ti.xcom_pull(task_ids="get_latest_sales_file_path", key="latest_sales_file") }}',
        # Only run if a file was found by the previous task
        do_xcom_push=False, # We're pulling an XCom, not pushing
        trigger_rule='all_success' # This task should only run if previous succeeds
    )

    # Task 4: Transform raw data and load into Data Warehouse (fact and dimension tables)
    transform_load_dwh = BashOperator(
        task_id='transform_and_load_data_warehouse',
        bash_command='python /opt/airflow/scripts/transform_load_dwh.py',
    )

    # Define the task dependencies
    generate_sales_data >> get_latest_sales_file_path >> ingest_raw_data >> transform_load_dwh

from airflow import DAG
import os
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow.utils.dates import datetime
import requests
import gzip
from sqlalchemy import create_engine
import sqlite3
from airflow.models import Variable
from wiki.funk import download_pageviews,filter_company_pageviews,load_data,check_file_exists,get_top_company

url = "https://dumps.wikimedia.org/other/pageviews/2024/2024-10/pageviews-20241010-160000.gz"

arg = {

"params": {
    "dag_owner": "Victor Aigbedion"
}
}

# Define the DAG
dag = DAG(
    start_date = datetime(2024, 10, 2),
    dag_id='wikipedia_pageviews',
    description='A straight DAG to download, extract, transform and process Wikipedia pageview data',
    schedule_interval=None,  
    catchup=False,
    default_args=arg
)


#Python operator that downloads the zip file
download_task = PythonOperator(
    task_id='download_and_extract_data',
    python_callable=lambda:download_pageviews(url,'/home/zizi/airflow/airbox/dags/wiki/pageviews.gz'),
    dag=dag,
)

#BashOperator to extract compressed file to pages.txt
unzip_task = BashOperator(
    task_id='unzip_pageviews',
    bash_command= 'gunzip -c /home/zizi/airflow/airbox/dags/wiki/pageviews.gz > /home/zizi/airflow/airbox/dags/wiki/pages.txt; echo "Successfully unzipped to pages.txt" || echo "Failed to unzip" ',
    dag=dag,
)

#Python operator that checks if file was truly downloaded 
check_file_task = PythonOperator(
    task_id='check_file_exists',
    python_callable=lambda:check_file_exists('/home/zizi/airflow/airbox/dags/wiki/pages.txt'),
    dag=dag,
)

#Python Operator that extracts the selected compainies and their page views into a .sql file (Insert.sql)
filter_task = PythonOperator(
    task_id='filter_task',
    python_callable=lambda:filter_company_pageviews('/home/zizi/airflow/airbox/dags/wiki/pages.txt','/home/zizi/airflow/airbox/dags/wiki/Insert.sql'),
    dag=dag,
)

#Python Operator that drops the pageviews table (if exists), creates another one and inserts values into the table
load_task = PythonOperator(
    task_id='load_data',
    python_callable=lambda:load_data('//home/zizi/airflow/airbox/dags/wiki/Insert.sql'),
    dag=dag,
)

#Python Operator that gets the top company by number of views
analyze_data_task = PythonOperator(
    task_id='analyze_data',
    python_callable=get_top_company,
    dag=dag,
)

#Set the order of execution of tasks.
download_task >> unzip_task >> check_file_task >>filter_task >> load_task >> analyze_data_task

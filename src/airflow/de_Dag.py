from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os

srcDir = '~/Wiki_Bias/src/ingestion/'
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 11, 16),
    'catch_up':False,
    'retries': 5,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'wiki_bias', default_args=default_args)

downloadData= BashOperator(
    task_id='download-urls-list',
    bash_command='python3 ' + srcDir + 'generate_text_file.py' ,
    dag=dag)
loaddatatobucket = BashOperator(
    task_id='load-zip-files',
    bash_command=   srcDir + './download.sh' ,
    dag=dag)

runSpark= BashOperator(
    task_id='run-spark-articles',
    bash_command='ssh ubuntu@10.0.0.4 /home/ubuntu/wiki_bias/src/dataprocessing/run_articles.sh',
    dag=dag)

runSpark2= BashOperator(
    task_id='run-spark-edit_history',
    bash_command='ssh ubuntu@10.0.0.4 /home/ubuntu/wiki_bias/src/dataprocessing/edit_history.sh',
    dag=dag)

sql_commands = BashOperator(
    task_id='sql-commands',
    bash_command='ssh ubuntu@10.0.0.14 /home/ubuntu/wiki_bias/src/analytics/edit_history.sh',
    dag=dag)

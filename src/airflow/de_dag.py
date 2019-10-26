from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os



srcDir = '/home/ubuntu/stackInsight/s3'
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 7, 6),
    'retries': 5,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG(
    'stackins', default_args=default_args)

downloadData= BashOperator(
    task_id='download-urls-list',
    bash_command='python ' + srcDir + 'urls_retrieve.py' ,
    dag=dag)
loaddatatobucket = BashOperator(
    task_id='load-zip-files',
    bash_command=   srcDir + 'transfer_to_s3.sh ' ,
    dag=dag)

downloadData.set_downstream(loaddatatobucket)
filesconversion = BashOperator(
     task_id='convert-to-xml',
     bash_command='python ' + srcDir + 's3_xml.py',
     dag=dag)
loaddatatobucket.set_downstream(filesconversion)

cmd_posts_pr = "ssh ubuntu@10.0.0.13 /usr/local/spark/bin/spark-submit \
   --master spark://ip-10-0-0-13:7077 \
   --deploy-mode cluster \
   --executor-memory 20G \
   --driver-memory 8G \
   --total-executor-cores 4 \
   --jars postgresql-9.4.1207.jar,aws-java-sdk-1.7.4.jar,hadoop-aws-2.7.3.jar \
   /home/ubuntu/stackInsights/spark/posts_xml_parq.py"


posts_p = BashOperator(
     task_id='posts-parquet-sparks',
     bash_command=cmd_posts_pr
     dag=dag)
posts_p.set_downstream(filesconversion)


cmd_posts_pr = "ssh ubuntu@10.0.0.13 /usr/local/spark/bin/spark-submit \
   --master spark://ip-10-0-0-13:7077 \
   --deploy-mode cluster \
   --executor-memory 20G \
   --driver-memory 8G \
   --total-executor-cores 4 \
   --jars postgresql-9.4.1207.jar,aws-java-sdk-1.7.4.jar,hadoop-aws-2.7.3.jar \
   /home/ubuntu/stackInsights/spark/links_xml_parq.py"


links_p = BashOperator(
     task_id='links-parquet-sparks',
     bash_command=cmd_links_pr
     dag=dag)
links_p.set_downstream(posts_p)



cmd_pr_spark = "ssh ubuntu@10.0.0.13 /usr/local/spark/bin/spark-submit \
   --master spark://ip-10-0-0-13:7077 \
   --deploy-mode cluster \
   --executor-memory 20G \
   --total-executor-cores 4 \
   --jars postgresql-9.4.1207.jar,aws-java-sdk-1.7.4.jar,hadoop-aws-2.7.3.jar \
   --packages graphframes:graphframes:0.5.0-spark2.1-s_2.1 \
   /home/ubuntu/stackInsights/spark/pagerank_calculation.py"
   
pr_calculation = BashOperator(
     task_id='page-rank-sparks',
     bash_command=cmd_pr_spark
     dag=dag)
pr_calculation.set_downstream(links_p)  
   

cmd_df_join = "ssh ubuntu@10.0.0.13 /usr/local/spark/bin/spark-submit \
   --master spark://ip-10-0-0-13:7077 \
   --deploy-mode cluster \
   --executor-memory 20G \
   --driver-memory 8G \
   --total-executor-cores 6 \
   --jars postgresql-9.4.1207.jar,aws-java-sdk-1.7.4.jar,hadoop-aws-2.7.3.jar \
   /home/ubuntu/stackInsights/spark/join_dfs.py"
df_join_spark = BashOperator(
     task_id='join-spark-df',
     bash_command=cmd_df_join
     dag=dag)
df_join_spark.set_downstream(pr_calculation)


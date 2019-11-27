'''
Sample input:
spark-submit --master spark://ec2-18-235-14-71.compute-1.amazonaws.com:7077 --jars postgresql-42.2.8.jar --packages com.databricks:spark-xml_2.11:0.6.0,org.postgresql:postgresql:42.2.5 main.py metahistory test_table test_article
Test with metacurrent:
spark-submit --master spark://ec2-18-235-14-71.compute-1.amazonaws.com:7077 --jars postgresql-42.2.8.jar --packages com.databricks:spark-xml_2.11:0.6.0,org.postgresql:postgresql:42.2.5 main.py metacurrent test_talk test_article
'''
import os
import sys
import time
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, size, explode, isnull, udf, desc, expr, lit
import re
from pyspark.sql import *

'''
Parses references XML file from S3 bucket
to Postgres.
'''

def count_reverts(comments_array):
    reverts_count = 0
    for comment in comments_array:  # print(type(text))
        try:
            match_list = re.findall('(?i)(revert)', comment)
            reverts_count += len(match_list)
        except:
            pass
    return reverts_count
def count_bots(username_array):
    bots_count = 0
    for username in username_array:  # print(type(text))
        try:
            match_list = re.findall('(?i)(bot)', username)
            bots_count += len(match_list)
        except:
            pass
    return bots_count
def count_reverts_ind(comment):
    reverts_count = 0
    try:
        match_list = re.findall('(?i)(revert)', comment)
        reverts_count += len(match_list)
    except:
        pass
    return reverts_count
def count_bots_ind(username):
    bots_count = 0
    try:
        match_list = re.findall('(?i)(bot)', username)
        bots_count += len(match_list)
    except:
        pass
    return bots_count

def get_reverts_article(wikipedia,filter_date):
    article_edit = wikipedia.filter("ns = '0'", "REVISION.TIMESTAMP >"+str(filter_date))
    article_edit.createTempView('article')
    article_edit = spark.sql("SELECT ID AS ENTITY_ID, TITLE AS ENTITY_TITLE, REVISION AS REVISION, REVISION.ID AS REVISIONIDS, REVISION.CONTRIBUTOR.USERNAME AS USERNAME, REVISION.COMMENT._VALUE AS COMMENT FROM article")
    find_reverts_udf = udf(count_reverts, IntegerType())  # type: object
    find_bots_udf = udf(count_bots, IntegerType())  # type: object
    article_edit = article_edit.withColumn('reverts', find_reverts_udf(article_edit.COMMENT))
    article_edit = article_edit.withColumn('bots', find_bots_udf(article_edit.USERNAME))
    article_edit = article_edit.select(col('entity_id'), col('entity_title'),col('reverts'), size(article_edit.REVISION).alias('nofedits'),size(article_edit.REVISIONIDS).alias('nofedits_ids'), col('bots'), col('revision'))
    article_revs = article_edit.withColumn("revision", explode(article_edit.revision))
    article_revs.createTempView('article_revs')
    article_revs = spark.sql("SELECT ENTITY_ID, ENTITY_TITLE, REVISION.TIMESTAMP AS TIME_STAMP, NOFEDITS,REVERTS,BOTS, REVISION.CONTRIBUTOR.USERNAME AS USERNAME, REVISION.COMMENT._VALUE AS COMMENT FROM article_revs")
    find_reverts_udf_ind = udf(count_reverts_ind, IntegerType())  # type: object
    find_bots_udf_ind = udf(count_bots_ind, IntegerType())  # type: object
    article_revs = article_revs.withColumn('reverts_ind', find_reverts_udf_ind(article_revs.COMMENT))
    article_revs = article_revs.withColumn('bots_ind', find_bots_udf_ind(article_revs.USERNAME))
    return article_revs

user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
hostIP = os.environ["POSTGRES_HOSTNAME"]
database = os.environ["POSTGRES_DBNAME"]

properties = {
    "user": user,
    "password": password,
    "driver": "org.postgresql.Driver"
}

port = "5432"
url = "jdbc:postgresql://{0}:{1}/".format(hostIP, port)
def write2postgres(df, table):
    print(properties)
    df.select('time_stamp','entity_id', 'reverts','nofedits','username','bots','reverts_ind','bots_ind'). \
        write.jdbc(url=url, table=table,
                   mode='append', properties=properties)
# Parse file
if __name__ == '__main__':
    file_name = sys.argv[1]
    postgres_table_name_talk = sys.argv[2]
    filter_date = sys.argv[3]
    num_file = sys.argv[4]
    spark = SparkSession.builder.getOrCreate()
    file = "s3a://wikibuckets/stub/enwiki-20190901-stub-meta-history"+str(num_file)+".xml"
    wikipedia = spark.read.format('xml') \
        .options(rowTag='page').load(file)
    # Parse articles
    references_dataframe_article = get_reverts_article(wikipedia,filter_date)
    df =references_dataframe_article
    write2postgres(df = references_dataframe_article, table = postgres_table_name_article)

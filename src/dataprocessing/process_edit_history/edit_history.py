# import parse_refs
# import export2postgres
import sys
# import os
'''
Sample input:
spark-submit --master spark://ec2-18-235-14-71.compute-1.amazonaws.com:7077 --jars postgresql-42.2.8.jar --packages com.databricks:spark-xml_2.11:0.6.0,org.postgresql:postgresql:42.2.5 main.py metahistory test_table test_article
Test with metacurrent:
spark-submit --master spark://ec2-18-235-14-71.compute-1.amazonaws.com:7077 --jars postgresql-42.2.8.jar --packages com.databricks:spark-xml_2.11:0.6.0,org.postgresql:postgresql:42.2.5 main.py metacurrent test_talk test_article
'''
# from pyspark.sql import SparkSession, functions as fs
# SparkSession.builder.getOrCreate().sparkContext.setLogLevel("ERROR")
import os
import sys
import time
from pyspark.sql import SparkSession
from pyspark.sql.types import *
# from pyspark.sql.functions import explode
# from pyspark import SparkContext
# from pyspark.sql import SQLContext
# from pyspark.sql.types import TimestampType, ArrayType, StringType
from pyspark.sql.functions import col, size, explode, isnull, udf, desc, expr, lit
# from mwcites.extractors import arxiv, doi, isbn, pubmed
import re
# import pyspark.sql
from pyspark.sql import *
# import pandas as pd
# import matplotlib.pyplot as plt
# import hashlib
# import os.path
# from datetime import timedelta, date
# import hashlib
# from urllib.parse import urlparse
# import pyspark.sql.functions as sf
# from operator import add

'''
Parses references XML file from S3 bucket
to Postgres.
'''
# def print_df_count(df):
#     print('printSchema --------------------------')
#     df.printSchema()
#     print('df.count(), len(df.columns) --------------------------')
#     print(df.count(), len(df.columns))
#     print('df show() ---------------------------')
#     df.show()
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

def get_reverts_article(wikipedia):
    article_edit = wikipedia.filter("ns = '0'")
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
    article_revs.printSchema()
    # df_page_count_reverts_articles = article_edit.groupby("entity_id","timestamp").agg({"reverts": "sum","nofedits":"sum","bots":"sum")
    # article_revs = article_revs.withColumn("time_stamp", article_revs.time_stamp.cast(TimestampType()))
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
# url = 'jdbc:postgresql://ec2-3-222-98-195.compute-1.amazonaws.com:5432/'

def write2postgres(df, table):
    # print_df_count(df)
    print(properties)
    #'timestamp'),col('entity_id'), col('reverts'), size(article_edit.REVISION).alias('nofedits'),size(article_edit.REVISIONIDS).alias('nofedits_ids'), col('username'), col('bots'))
    df.select('time_stamp','entity_id', 'reverts','nofedits','username','bots','reverts_ind','bots_ind'). \
        write.jdbc(url=url, table=table,
                   mode='append', properties=properties)
# Parse file
if __name__ == '__main__':
    file_name = sys.argv[1]
    postgres_table_name_talk = sys.argv[2]
    postgres_table_name_article = sys.argv[3]
    start_time = time.time()
    num_file = sys.argv[4]
    spark = SparkSession.builder.getOrCreate()
    files = {}
    files['metahistory'] = "s3a://wikibuckets/enwiki_sub/enwiki-20190901-pages-meta-history1.xml-p5406p6201"
    files['metacurrent'] = "s3a://wikibuckets/enwiki_sub/enwiki-20190901-pages-meta-current1.xml-p10p30303.bz2"
    files['multistream'] = "s3a://wikibuckets/wikidata/enwiki-latest-pages-articles-multistream.xml.bz2'"
    files['m1'] = 's3a://wikibuckets/wikidata/enwiki-20190901-pages-articles-multistream1.xml-p10p30302'
    files['stub'] = "s3a://wikibuckets/stub/enwiki-20190901-stub-meta-history.xml"
    files['stub'+str(num_file)] = "s3a://wikibuckets/stub/enwiki-20190901-stub-meta-history"+str(num_file)+".xml"
    # files['stub1gz'] = "s3a://wikibuckets/stub/enwiki-20190901-stub-meta-history1.xml.gz"
    # print('file_name ----------------------------\n\n\n\n\n\n\n','stub'+str(num_file))
    file = files[str(file_name)]
    print(file)
    wikipedia = spark.read.format('xml') \
        .options(rowTag='page').load(file)
    read_end = time.time()
    time_log = dict()
    time_log['read_elapsed'] = time.time() - start_time
    # print('Total elapsed time was {:5.4f}s'.format(time_log['read_elapsed']))

    # Parse talks
    talk_end = time.time()
    time_log['talk_elapsed'] = talk_end - read_end
    # print('Talk elapsed time was {:5.4f}s'.format(time_log['talk_elapsed']))

    # Parse articles
    references_dataframe_article = get_reverts_article(wikipedia)
    df =references_dataframe_article
    # df.withColumn('ratio',df.reverts/df.nofedits)
    # df = df.withColumn('bot_ratio',df.bots/df.nofedits)
    articles_end = time.time()
    time_log['articles_elapsed'] = articles_end - talk_end
    # print('Articles parsing elapsed time was {:5.4f}s'.format(time_log['articles_elapsed']))

    write2postgres(df = references_dataframe_article, table = postgres_table_name_article)

    postgres_end = time.time()
    time_log['postgres_elapsed'] = postgres_end - articles_end
    ## Summarizers
    # compute statistics for multiple metrics without weight
    # from pyspark.ml.stat import Summarizer
    # from pyspark.sql import Row
    # from pyspark.ml.linalg import Vectors

    # Summarizer
    # summarizer = Summarizer.metrics("mean", "count")
    # df = summarizer.summary(df.reverts,df.nofedits).show(truncate=False)
    # df.write.jdbc(url=url, table='summary',
    #                mode='append', properties=properties)
    # from pyspark.ml.linalg import Vectors
    # from pyspark.ml.stat import Correlation
    # r1 = Correlation.corr(df, "reverts", "nofedits")
    # r1head = r1.head()
    # print("Pearson correlation matrix:\n" + str(r1head[0]))

    # r2 = Correlation.corr(df, "spearman")
    # r2head = r2.head()
    # print("Spearman correlation matrix:\n" + str(r2head[0]))
    # r2.write.jdbc(url=url, table='summary_corr',
    #                mode='append', properties=properties)

    print('Postgres elapsed time was {:5.4f}s'.format(time_log['postgres_elapsed']))
    time_log['total_elapsed'] = time.time() - start_time
    print('Summary ----------- \n Total elapsed time was {:5.4f}s'.format(time_log['total_elapsed']))
    print('Reading from s3 elapsed time was {:5.4f}s'.format(time_log['read_elapsed']))
    print('Talk from s3 elapsed time was {:5.4f}s'.format(time_log['talk_elapsed']))
    print('Articles elapsed time was {:5.4f}s'.format(time_log['articles_elapsed']))
    print('Postgres elapsed time was {:5.4f}s'.format(time_log['postgres_elapsed']))
    with open('stub_log' + str(num_file) + '.csv', 'w') as f:
        for key in time_log.keys():
            f.write("%s,%s\n" % (key, time_log[key]))
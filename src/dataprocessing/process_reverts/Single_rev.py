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
def print_df_count(df):
    print('printSchema --------------------------')
    df.printSchema()
    print('df.count(), len(df.columns) --------------------------')
    print(df.count(), len(df.columns))
    print('df show() ---------------------------')
    df.show()

def count_reverts(text):
    try:
        print(type(text))
        match_list = re.findall('(?i)(revert)', text)
        #       reverts = map(lambda x: x, match_list)
        revert_count = len(match_list)
    #         revert_count = len(match_lists
        return revert_count
    except:
        return int(0)

def get_reverts_talk(wikipedia):
    talk = wikipedia.filter("ns = '1'")
    talk.createTempView('temp_talk1')
    talk_2 = spark.sql("SELECT ID AS TALK_ID, TITLE AS TALK_TITLE, REVISION.COMMENT FROM temp_talk1")
    talk_2.printSchema()
    talk_filtered = talk_2.filter("comment is not null")
        # .filter("length(comment) > 0")
    talk_filtered.show()
    print((talk_filtered.count(), len(talk_filtered.columns)))
    find_reverts_udf = udf(count_reverts, IntegerType())  # type: object
    # find reverts from the comments column using regex with udf
    talk_filtered = talk_filtered.withColumn('nofedits', lit(1))
    talk_filtered = talk_filtered.withColumn('reverts', find_reverts_udf(talk_filtered.COMMENT))
    talk_filtered = talk_filtered.select(col('talk_id'),
                                              col('talk_title'),
                                              col('reverts'),col('nofedits'))
    talk_filtered = talk_filtered.withColumn("entity_title",
                                                             expr("substring(talk_title, 6, length(talk_title))"))
    df_page_count_reverts_talk = talk_filtered.groupby("entity_title").agg({"reverts": "sum", "nofedits": "count"})
    print('df_page_count_reverts-------------------------')
    print_df_count(df_page_count_reverts_talk)
    return df_page_count_reverts_talk

def get_reverts_article(wikipedia):
    article_edit = wikipedia.filter("ns = '0'")
    article_edit.createTempView('temp_talk7')
    article_edit = spark.sql("SELECT ID AS ENTITY_ID, TITLE AS ENTITY_TITLE, REVISION.COMMENT FROM temp_talk7")
    article_edit.printSchema()
    article_filtered = article_edit.filter("comment is not null")
        # .filter("length(comment) > 0")
    article_filtered.show()
    print((article_filtered.count(), len(article_filtered.columns)))

    find_reverts_udf = udf(count_reverts, IntegerType())  # type: object
    # find reverts from the comments column using regex with udf
    article_filtered = article_filtered.withColumn('nofedits', lit(1))
    article_filtered = article_filtered.withColumn('reverts', find_reverts_udf(article_filtered.COMMENT))
    article_filtered = article_filtered.select(col('entity_id'),
                                                               col('entity_title'),
                                                               col('reverts'),col('nofedits'))
    df_page_count_reverts_articles = article_filtered.groupby("entity_id","entity_title").agg({"reverts":"sum","nofedits":"count"})
    print('df_page_count_reverts------------------------')
    print_df_count(df_page_count_reverts_articles)
    return df_page_count_reverts_articles


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
    print_df_count(df)
    print(properties)
    df.select('entity_id', 'entity_title', 'reverts'). \
        write.jdbc(url=url, table=table,
                   mode='overwrite', properties=properties)

def write2postgres_talk(df, table):
    print_df_count(df)
    print(properties)
    df.select('entity_title', 'reverts'). \
        write.jdbc(url=url, table=table,
                   mode='overwrite', properties=properties)


# Parse file
if __name__ == '__main__':
    file_name = sys.argv[1]
    postgres_table_name_talk = sys.argv[2]
    postgres_table_name_article = sys.argv[3]

    spark = SparkSession.builder.getOrCreate()

    files = {}
    files['metahistory'] = "s3a://wikibuckets/enwiki_sub/enwiki-20190901-pages-meta-history1.xml-p5406p6201"
    files['metacurrent'] = "s3a://wikibuckets/enwiki_sub/enwiki-20190901-pages-meta-current1.xml-p10p30303.bz2"
    files['multistream'] = "s3a://wikibuckets/wikidata/enwiki-latest-pages-articles-multistream.xml.bz2'"
    files['stub1'] = "s3a://wikibuckets/stub/enwiki-20190901-stub-meta-history1.xml"
    # files['stub1gz'] = "s3a://wikibuckets/stub/enwiki-20190901-stub-meta-history1.xml.gz"

    file = files[file_name]
    wikipedia = spark.read.format('xml') \
        .options(rowTag='page').load(file)
    references_dataframe_talk = get_reverts_talk(wikipedia)
    references_dataframe_article = get_reverts_article(wikipedia)
    write2postgres_talk(df = references_dataframe_talk, table = postgres_table_name_talk)
    write2postgres(df = references_dataframe_article, table = postgres_table_name_article)

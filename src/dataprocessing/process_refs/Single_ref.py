# from pyspark.sql import SparkSession, functions as fs
# SparkSession.builder.getOrCreate().sparkContext.setLogLevel("ERROR")
import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import explode
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import TimestampType, ArrayType, StringType
from pyspark.sql.functions import col, size, explode, isnull, udf, desc
from mwcites.extractors import arxiv, doi, isbn, pubmed
import export2postgres
import re
import pyspark.sql
from pyspark.sql import *
# import pandas as pd
# import matplotlib.pyplot as plt
import hashlib
import os.path
from datetime import timedelta, date
import hashlib
from urllib.parse import urlparse
import pyspark.sql.functions as sf
from operator import add
import time

start_time = time.time()
'''
Parses one XML file from S3 bucket
to Postgres.
'''
def print_df_count(df):
    print('printSchema --------------------------')
    df.printSchema()
    print('df.count(), len(df.columns) --------------------------')
    print(df.count(), len(df.columns))
    print('df show() ---------------------------')
    df.show()

# s3://wikibuckets/wikidata/enwiki-latest-pages-articles-multistream.xml.bz2
wikipedia_dump = "s3a://wikibuckets/wikidata/enwiki-latest-pages-articles-multistream.xml.bz2"
# metacurrent = "s3a://wikibuckets/enwiki_sub/enwiki-20190901-pages-meta-current1.xml-p10p30303.bz2"
# metahistory = "s3a://wikibuckets/enwiki_sub/enwiki-20190901-pages-meta-history1.xml-p5406p6201"
# multistream = 's3a://wikibuckets/wikidata/enwiki-20190901-pages-articles-multistream1.xml-p10p30302.bz2'
# wikipedia_dump = 's3a://wikibuckets/wikidata/enwiki-20190901-pages-articles-multistream1.xml-p10p30302.bz2'

spark = SparkSession.builder.getOrCreate()
wikipedia = spark.read.format('xml')\
   .options(rowTag='page').load(wikipedia_dump)

read_end = time.time()

read_elapsed = time.time() - start_time
print('Total elapsed time was {:5.4f}s'.format(read_elapsed))

ref_regex = re.compile(r'(<ref[^>]*[^/]>|<ref[ ]*>){{([^<]*)}}</ref')

def get_refs_info(entity):
    text = entity.revision.text._VALUE
    text = re.sub("(<!--.*?-->)", "", text, flags=re.MULTILINE) # remove comments
    refs = ref_regex.findall(text)
    result = []
    for r in refs:
        ref_content = r[1].split(r"|")
        template = ref_content.pop(0).strip()
        properties = {}
        for p in ref_content:
            eq_index = p.find("=")
            p_name = p[0:eq_index].strip()
            p_value = p[eq_index+1:].strip()
            properties[p_name] = p_value
        result.append(Row(id=entity.id,entity_title =entity.title,
                          template=template.lower(),
                          template_original=template,
                          url=properties.get("url", ""),
                          title=properties.get("title")))
    return result


articles = wikipedia.filter("ns = '0'").filter("redirect._title is null") \
    .filter("revision.text._VALUE is not null") \
    .filter("length(revision.text._VALUE) > 0")

references_rrd = articles.rdd.flatMap(get_refs_info)

references = spark.createDataFrame(references_rrd)
references.show()

df = references
# filename='./ref_spdf_4.py'
# df.rdd.saveAsPickleFile(filename)
# To load it from file, run:
# pickleRdd = sc.pickleFile(filename).collect()
# df2 = spark.createDataFrame(pickleRdd)

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

print_df_count(df)

# export2postgres.write_reverts_postgres(df_reverts = df, jdbc_url=url,
# connection_properties=properties)

processing_end = time.time()
process_elapsed = processing_end - read_end
print('Processing time was {:5.4f}s'.format(process_elapsed))

print(properties)
df.select('id', 'entity_title', 'template','template_original','url','title').\
    write.jdbc(url=url, table='table_name_n',
               mode='overwrite', properties=properties)
load_end = time.time()
elapsed_postgres = load_end - processing_end

print('Postgres elapsed time was {:5.4f}s'.format(elapsed_postgres))

total_elapsed = time.time() - start_time
print('Summary ----------- \n Total elapsed time was {:5.4f}s'.format(total_elapsed))
print('Processing time was {:5.4f}s'.format(process_elapsed))
print('Reading from s3 elapsed time was {:5.4f}s'.format(read_elapsed))

# import dependencies
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
# from pyspark.sql.functions import col, size, explode, isnull, udf, desc, expr, lit
# from mwcites.extractors import arxiv, doi, isbn, pubmed
import re
# import pyspark.sql
from pyspark.sql import *
# import categories from MariaDB
# import references from PostgreSQL
load_begin = time.time()

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

# _select_sql = "select * from database_name.conflict"
spark = SparkSession.builder.getOrCreate()
conflict = spark.read.jdbc(url=url,table='conflict',properties=db_properties)
table_references = spark.read.jdbc(url=url,table='table_references',properties=db_properties)
#print_df_count(df)
merged = table_references.join(conflict, table_references.id == conflict.entity_id)

merged.write.jdbc(url=url, table=table,
                   mode='append', properties=properties)#print_df_count(df)

time_log = {}
load_end = time.time()
time_log['merge_elapsed'] = load_start -load_end
print('Postgres elapsed time was {:5.4f}s'.format(time_log['merge_elapsed']))

with open('stub_log' + str(num_file) + '.csv', 'w') as f:
    for key in time_log.keys():
        f.write("%s,%s\n" % (key, time_log[key]))
#
# # export2postgres.write_reverts_postgres(df_reverts = df, jdbc_url=url,
# # connection_properties=properties)
#
# processing_end = time.time()
# process_elapsed = processing_end - read_end
# print('Processing time was {:5.4f}s'.format(process_elapsed))
#
# print(properties)
# df.select('id', 'entity_title', 'template','template_original','url','title').\
#     write.jdbc(url=url, table='table_name_n',
#                mode='overwrite', properties=properties)
# load_end = time.time()
# elapsed_postgres = load_end - processing_end
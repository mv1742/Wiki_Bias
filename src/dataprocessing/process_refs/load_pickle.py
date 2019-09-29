# from pyspark.sql import SparkSession, functions as fs
# SparkSession.builder.getOrCreate().sparkContext.setLogLevel("ERROR")
# import os
# import sys
# from pyspark.sql import SparkSession
from pyspark.sql.types import *
# from pyspark.sql.functions import explode
# from pyspark import SparkContext
# from pyspark.sql import SQLContext
# from pyspark.sql.types import TimestampType, ArrayType, StringType
# from pyspark.sql.functions import col, size, explode, isnull, udf, desc
# from mwcites.extractors import arxiv, doi, isbn, pubmed
# import export2postgres
# import re
# import pyspark.sql
from pyspark.sql import *
import os.path
import time
from pyspark import SparkFiles
from pyspark import SparkContext
sc =SparkContext.getOrCreate()
spark = SparkSession.builder.getOrCreate()


start_time = time.time()

filename='./ref_spdf_3.p'

# To load it from file, run:
pickleRdd = sc.pickleFile(filename).collect()
df2 = spark.createDataFrame(pickleRdd)

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
elapsed_postgres = processing_end - load_end
print('Postgres elapsed time was {:5.4f}s'.format(elapsed_postgres))

total_elapsed = time.time() - start_time
print('Summary ----------- \n Total elapsed time was {:5.4f}s'.format(total_elapsed))
print('Processing time was {:5.4f}s'.format(process_elapsed))
print('Reading from s3 elapsed time was {:5.4f}s'.format(read_elapsed))

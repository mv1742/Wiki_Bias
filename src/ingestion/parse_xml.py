from pyspark.sql import SparkSession, functions as fs
SparkSession.builder.getOrCreate().sparkContext.setLogLevel("ERROR")
import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import explode
import psycopg2
'''
Parses one XML file from S3 bucket
to Postgres.
'''
def main(num):
	spark = SparkSession.builder.getOrCreate()
	df_raw = spark.read.format("xml") \
		.options(rowTag="text", excludeAttribute=True) \
		.load("s3a://wikibuckets/enwiki_sub/enwiki-20190901-pages-meta-current14.xml-p7697598p7744799") \
		.persist()
	print(spark.catalog.listTables())
	print(df_raw)
	connectionProperties = {
		"user": os.environ["POSTGRES_USER"],
		"password": os.environ["POSTGRES_PASSWORD"],
		"driver":"org.postgresql.Driver"
	}
	jdbcHostname = os.environ["POSTGRES_URL"]
	jdbcDatabase = os.environ["POSTGRES_DBNAME"]
	jdbcPort = "5432"
	jdbcUrl = "jdbc:postgresql://{0}:{1}/{2}".format(jdbcHostname, jdbcPort, jdbcDatabase)
	df.select("id", "text", "time", "contributor.username") \
		.write.jdbc(url=jdbcUrl, table="history"+num, properties=connectionProperties, mode="overwrite")

if __name__ == '__main__':
	os.environ["POSTGRES_URL"] = sys.argv[2]
	os.environ["POSTGRES_USER"] = sys.argv[3]
	os.environ["POSTGRES_PASSWORD"] = sys.argv[4]
	os.environ["POSTGRES_DBNAME"] = sys.argv[5]
	main(sys.argv[1])


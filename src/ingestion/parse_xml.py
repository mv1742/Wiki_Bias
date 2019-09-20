from pyspark.sql import SparkSession, functions as fs
SparkSession.builder.getOrCreate().sparkContext.setLogLevel("ERROR")
import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import explode
import psycopg2
#import psycopg2
'''
Parses one XML file from S3 bucket
to TimescaleDB.
'''
#ACCESS_KEY = "AKIAZ4LCPHIH4IUQA5OB"
#SECRET_KEY = "f8X.......+b"
#ENCODED_SECRET_KEY = SECRET_KEY.replace("/", "%2F")
#AWS_BUCKET_NAME = "wikibuckets"
#MOUNT_NAME = "mounting_test"

#dbutils.fs.mount("s3a://%s:%s@%s" % (ACCESS_KEY, ENCODED_SECRET_KEY, AWS_BUCKET_NAME), "/mnt/%s" % MOUNT_NAME)
#display(dbutils.fs.ls("/mnt/%s" % MOUNT_NAME))

def main(num):
	spark = SparkSession.builder.getOrCreate()
	df_raw = spark.read.format("xml") \
		.options(rowTag="text", excludeAttribute=True) \
		.load("s3a://wikibuckets/enwiki_sub/enwiki-20190901-pages-meta-current14.xml-p7697598p7744799") \
		.persist()
#	df_raw2 = spark.read.format("xml") \
#		.options(rowTag="pages") \
#		.load("s3a//wikibuckets/enwiki_sub/enwiki-20190901-pages-meta-current14.xml-p7697598p7744799") \
#		.persist()
	print(spark.catalog.listTables())
	print(df_raw)
	
#	print(df_raw2)
	#.load("s3://wikibuckets/enwiki_sub/enwiki-20190901-pages-meta-history1.xml-p6202p7099.bz2") \
	#.persist()
        # convert time string to timestamp
	#df = df_raw.withColumn("time", df_raw.timestamp.cast(TimestampType())
	#print(df_raw.columns())
	#for row in df_raw.head(5):
	   # print(row)
	   # print('\n')
	#print(df_raw.Schema)
	#print('df.show() ----------------------------------------------------\n\n\n\n\n\')
	#print('print df ------------------ \n\n\n\n\n\n\n', df.collect())
	#postgres credentials
	#	print(os.environ['POSTGRES_USER'])
	connectionProperties = {
		"user": os.environ["POSTGRES_USER"],
		"password": os.environ["POSTGRES_PASSWORD"],
		"driver":"org.postgresql.Driver"
	}
#	jdbcHostname = os.environ["POSTGRES_URL"]
#	jdbcDatabase = os.environ["POSTGRES_DBNAME"]
#	jdbcPort = "5432"
#	jdbcUrl = "jdbc:postgresql://{0}:{1}/{2}".format(jdbcHostname, jdbcPort, jdbcDatabase)
	#df.select("id", "text", "time", "contributor.username") \
	#	.write.jdbc(url=jdbcUrl, table="history"+num, properties=connectionProperties, mode="overwrite")
	#import psycopg2
	connection = psycopg2.connect(host = '10.0.0.14', database = 'postgres', user = 'postgres', password = 'Sapr2019')
        #connection = psycopg2.connect(host = '127.0.0.1', database = 'test', user = 'postgres', password = 'MYPASSWORD')
	cursor = connection.cursor()
	cursor.execute('''INSERT INTO playground (equip_id, type, color, location) values (21, 'see-saw', 'red', 'north')''')
	connection.commit() # Important!
	cursor.execute('''SELECT * FROM playground''')
	print(cursor.fetchall())
	cursor.close()
	connection.close()



if __name__ == '__main__':
	os.environ["POSTGRES_URL"] = sys.argv[2]
	os.environ["POSTGRES_USER"] = sys.argv[3]
	os.environ["POSTGRES_PASSWORD"] = sys.argv[4]
	os.environ["POSTGRES_DBNAME"] = sys.argv[5]
	main(sys.argv[1])


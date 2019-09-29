# import dependencies

# import categories from MariaDB
# import references from PostgreSQL
user = os.environ["MARIA_USER"]
password = os.environ["MARIA_PASSWORD"]
hostIP = os.environ["MARIA_HOSTNAME"]
database = os.environ["MARIA_DBNAME"]

properties = {
    "user": user,
    "password": password,
    "driver": "org.mariadb.jdbc.Driver"
}

port = "5432"
url = "jdbc:mysql://{0}:{1}/".format(hostIP, port)
# url = 'jdbc:mysql://ec2-3-222-98-195.compute-1.amazonaws.com:5432/'

_select_sql = "(select * from database_name.category"
df_select = spark.read.jdbc(url=url,table=_select_sql,properties=db_properties)
df = spark.read.jdbc(url=url,table='category',properties=db_properties)


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

# import reverts


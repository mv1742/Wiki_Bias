import os
import sys
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.types import TimestampType, ArrayType, StringType
from pyspark.sql.functions import col, size, explode, isnull, udf, desc
import re
from pyspark.sql import *
import os.path
import time

# Parse articles to obtain references, infobox, length, and categories
def get_arts_info(entity):
    ref_regex = re.compile(r'(<ref[^>]*[^/]>|<ref[ ]*>){{([^<]*)}}</ref')
    text = entity.revision.text._VALUE
    len_text = len(text)
    timestamp = entity.revision.timestamp
    cats_regex = re.compile("(?<=\[\[Category:)([^\n\r][^\]\]]*)")
    cats = cats_regex.findall(text)
    infobox_regex = re.compile("(?<={{infobox\s)(\w+)")
    infobox = infobox_regex.findall(text)
    text_refs = re.sub("(<!--.*?-->)", "", text, flags=re.MULTILINE) # remove comments
    refs = ref_regex.findall(text_refs)
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
        for ib in infobox:
            result.append(Row(id=entity.id,len_text=len_text,timestamp=timestamp,entity_title =entity.title,
                          template=template.lower(),
                          template_original=template,
                          url=properties.get("url", ""),
                          title=properties.get("title"), infobox=ib,categories=cats))
    return result

# Wrtie to Postgres database
def write2postgres(df, table=None):
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

    df.select('id', 'entity_title', 'len_text', 'template', 'time_stamp', 'template_original', 'url', 'title',
              'infobox', 'categories'). \
        write.jdbc(url=url, table='refs_cats_lens_infobox',
                   mode='append', properties=properties)

if __name__ == '__main__':
    # Read file name argument
    file_name = sys.argv[1]

    # Record time for benchmarking
    start_time = time.time()

    '''
    Parses one XML file from S3 bucket
    to Postgres.
    '''
    wikipedia_dump = "s3a://wikibuckets/wikidata/" + str(file_name)

    # initialize spark session
    spark = SparkSession.builder.getOrCreate()

    # read file using spark-xml
    wikipedia = spark.read.format('xml') \
        .options(rowTag='page').load(wikipedia_dump)

    read_end = time.time()
    time_log = {}
    time_log['read_elapsed'] = time.time() - start_time

    # filter articles
    articles = wikipedia.filter("ns = '0'").filter("redirect._title is null") \
        .filter("revision.text._VALUE is not null") \
        .filter("length(revision.text._VALUE) > 0")

    filter_end = time.time()
    time_log['filter_elapsed'] = filter_end - read_end

    articles_rrd = articles.rdd.flatMap(get_arts_info)

    articles = spark.createDataFrame(references_rrd)
    articles = articles.withColumn("time_stamp", references.timestamp.cast(TimestampType()))
    find_url_udf = udf(getdomain(url), StringType())  # type: object
    articles = articles.withColumn('domain', find_url_udf(references.url))
    df = articles


    # Regex time
    processing_end = time.time()
    time_log['regex_elapsed'] = processing_end - filter_end

    write2postgres(df = articles)

    # All processing time
    postgres_end = time.time()
    time_log['postgres'] = postgres_end - processing_end

    with open('time_log.csv', 'w') as f:
        for key in time_log.keys():
            f.write("%s,%s\n"%(key,time_log[key]))
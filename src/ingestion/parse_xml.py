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
from pyspark.sql.functions import col, size, explode, isnull, udf
from mwcites.extractors import arxiv, doi, isbn, issn, pubmed
'''
Parses one XML file from S3 bucket
to Postgres.
'''
class ParseXML:
  def __init__(self, file):
    self.file = file
    self.spark = SparkSession.builder.getOrCreate()
    self.format = "xml"
    self.row_tag_revision = "revision"
    self.row_tag_page = 'page'
    self.row_tag_id = 'id'
    self.df_main_pages_text = self.get_page_text_column(print_table_info=True)
    self.page_df_text = self.get_page_text_column(print_table_info=True)  # data frame with text
    self.page_id_title = self.get_df_with_page_id_title(print_table_info=True)  # df only article title and ID
    self.page_id_citations = self.get_df_article_id_citations(print_table_info=True)  # page id and links in list
    self.page_df_id_citation_time = self.explode_citations(print_table_info=True)   # data frame with exploded links

    # parse xml and extract information under page tag, filter only main articles
  def get_page_df_from_xml(self, print_table_info: bool):
      page_df = self.spark.read\
          .format(self.format) \
          .option("excludeAttribute", "false")\
          .options(rowTag=self.row_tag_page)\
          .load(self.file)
      print('page_df --------------------------')
      print_df_count(page_df) if print_table_info else None
      # Filter only main articles by its namespace and pages that are not redirecting
      main_articles = page_df.filter((page_df.ns == 0) & (isnull('redirect')))
      print('main_articles --------------------------')
      print_df_count(main_articles) if print_table_info else None
      return main_articles

  # PAGE_ID: int, PAGE_TITLE: str, REVISION_ID: int, TIME_STAMP: timestamp, TEXT: list with 1 element
  def get_page_text_column(self, print_table_info: bool):
      df_main_pages = self.get_page_df_from_xml(print_table_info=print_table_info)
      df_articles_text = df_main_pages.select(col('id').alias('page_id'),
                                              col('title').alias('page_title'),
                                              col('revision.id').alias("revision_id"),
                                              col('revision.timestamp'),
                                              col('revision.text'))
      df_articles_text = df_articles_text.withColumn("time_stamp",
                                                     df_articles_text.timestamp.cast(TimestampType()))
      print('df_articles_text --------------------------')
      print_df_count(df_articles_text) if print_table_info else None
      return df_articles_text

  # PAGE ID: int, PAGE TITLE: str
  def get_df_with_page_id_title(self, print_table_info: bool):
      df_article_id_title = self.df_main_pages_text.select(col('page_id'),
                                                           col('page_title'),
                                                           col("time_stamp")).distinct()
      print('df_article_id_title _distinct--------------------------')
      print_df_count(df_article_id_title) if print_table_info else None
      return df_article_id_title

  # PAGE ID: int, arxiv, doi, isbn, issn, pubmed
  def get_df_article_id_citations(self, print_table_info: bool):
      find_citations_udf = udf(arxiv.extract, ArrayType(StringType()))
      # find links from the text column using regex with udf from df with text column
      df = self.page_df_text.withColumn('citations_arxiv', find_citations_udf(self.page_df_text.text))
      
      find_citations_udf = udf(doi.extract, ArrayType(StringType()))
      df = self.page_df_text.withColumn('citations_doi', find_citations_udf(self.page_df_text.text))
      
      find_citations_udf = udf(isbn.extract, ArrayType(StringType()))
      df = self.page_df_text.withColumn('citations_isbn', find_citations_udf(self.page_df_text.text))
      
      find_citations_udf = udf(issn.extract, ArrayType(StringType()))
      df = self.page_df_text.withColumn('citations_issn', find_citations_udf(self.page_df_text.text))
      
      find_citations_udf = udf(pubmed.extract, ArrayType(StringType()))
      df = self.page_df_text.withColumn('citations_pubmed', find_citations_udf(self.page_df_text.text))

      df_page_count_citations = df.select(col('page_id'),
                                      col('page_title'),
                                      col('time_stamp'),
                                      col('citations_arxiv'),
                                      size('citations_arxiv').alias('arxiv_count'),
                                      col('citations_doi'),
                                      size('citations_doi').alias('doi_count'),
                                      col('citations_isbn'),
                                      size('citations_isbn').alias('isbn_cnt'),
                                      col('citations_issn'),
                                      size('citations_issn').alias('issn_cnt'),
                                      col('citations_pubmed'),
                                      size('citations_pubmed').alias('pubmed_cnt'),
      
      print('df_page_count_citations --------------------------')
      print_df_count(df_page_count_citations) if print_table_info else None
      return df_page_count_citations
    
    

  # (each link is a row):  PAGE_ID: int, PAGE_TITLE: str, REVISION_ID: int, TIME_STAMP: timestamp, LINK: str
  def explode_citations(self, print_table_info: bool):
      # create column of single link name
      #
      df_id_citatin_time = self.page_id_citation.withColumn("citations", explode(self.page_id_citations.citations))
      # create dataframe with article id, revision timestamp, link name (dropping links)
      page_df_id_link_time = df_id_link_time.select(col('page_id'),
                                                    col('page_title'),
                                                    col('citation'))
      print('page_df_id_citation_time --------------------------')
      print_df_count(page_df_id_citation_time) if print_table_info else None
      return page_df_id_citation_time

  def count_unique_citations(self):
      citation_count_df = self.page_df_id_citation_time.groupBy('citation').count().orderBy('count', ascending=False)
      print('citation_count_df --------------------------')
      citation_count_df.show(10)
      return citation_count_df
          
  # return list of link titles from a text if exist, else return empty lis
def count_reverts(text):
  import re
  try:
    match_list = re.findall('(?i)(?<= |^)reverted(?= |$)', text[0])
    reverts = map(lambda x: x, match_list)
    revert_count = len(reverts)
    return revert_count
  except:
    list_empty = []
    return list_empty

# helper for printing dataframe number of rows and columns
def print_df_count(df):
  print('printSchema --------------------------')
  df.printSchema()
  print('df.count(), len(df.columns) --------------------------')
  print(df.count(), len(df.columns))
  df.show()

if __name__ == '__main__':
	os.environ["POSTGRES_URL"] = sys.argv[2]
	os.environ["POSTGRES_USER"] = sys.argv[3]
	os.environ["POSTGRES_PASSWORD"] = sys.argv[4]
	os.environ["POSTGRES_DBNAME"] = sys.argv[5]
	process = ParseXML(small_file)
	write_pages_to_postgres(df_pages=process.page_id_links, jdbc_url=url, connection_properties=properties)					
	


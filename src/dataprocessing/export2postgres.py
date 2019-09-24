# Export to Postgres with JDBC

def export_postgres(df_pages, df_citations):

  # write citations and count data frame from batch_process to postgres
  def write_citations_to_postgres(df_citations, jdbc_url, connection_properties):
      df_citations.select('page_id', 'page_title',\
      'citations_doi', 'doi_count',\
      'citations_arxiv','arxiv_count','citations_doi','doi_count', \ 
      'citations_isbn','isbn_cnt','citations_issn','issn_cnt',\
      'citations_pubmed','pubmed_cnt', 'reverts').\
          write.jdbc(url=jdbc_url,
                     table='citations',
                     properties=connection_properties,
                     mode='append')
      print("CITATIONS DONE")


  # write link and count data frame from batch_process to postgres
  def write_link_count_to_postgres(df_citations_aggregated, jdbc_url, connection_properties):
      df_links.select('citations_doi', 'doi_count'\
      'citations_arxiv','arxiv_count','citations_doi','doi_count', \ 
      'citations_isbn','isbn_cnt','citations_issn','issn_cnt',\
      'citations_pubmed','pubmed_cnt').
          write.jdbc(url=jdbc_url,
                     table='citation_count',
                     properties=connection_properties,
                     mode='append')
      print("CITATIONS DONE")
      
    def write_reverts_to_postgres(df_reverts, jdbc_url, connection_properties):
      df_links.select('page_id','reverts')
          write.jdbc(url=jdbc_url,
                     table='citation_count',
                     properties=connection_properties,
                     mode='append')
      print("REVERTS DONE")

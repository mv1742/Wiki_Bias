# Source of Conflict

## Insight Data Engineering 2019C
## Manrique Vargas (MV), mv1742@nyu.edu

<img src="https://raw.githubusercontent.com/mv1742/Wiki_Bias/master/figs/SoC.png" data-canonical-src="https://raw.githubusercontent.com/mv1742/Wiki_Bias/master/figs/SoC.png" width="180" height="120" />

| Go to -> *[Presentation slides](https://docs.google.com/presentation/d/1uzJ4H3GOEt4qJk-HOeshhaqHc4EtusS9e92oKj92rIo/edit?usp=sharing)*      |  Go to ->  *[Demo @ dataangel.me](http://dataangel.me/80)*          |
| ------------- |:-------------:|

1. [Introduction](README.md#-1.-Introduction)
1. [Motivation](README.md#-2.-Motivation)
1. [Requirements](README.md#-3.-Requirements)
1. [Pipeline](README.md#-4.-Pipeline)
1. [Architecture](README.md#-5.-Architecture)
1. [Data Source](README.md#-6.-Data-Source)
1. [Metrics](README.md#-7.-Metrics)
1. [Methodology](README.md#-8.-Methodology)
1. [Getting Started](README.md#-9.-Getting-Started)
1. [Dashboard](README.md#-10.-Dashboard)
1. [Analytics](README.md#-11.-Analytics)
1. [Setup Notes](README.md#-12.-Setup-Notes)
1. [Repo-directory-structure](README.md#-13.-Repo-directory-structure)


# 1. Introduction
Source of Conflict is a tool for Wikipedia users and moderators to analyze how some features affect the edit history. I calculate different metrics for and identify which metrics lead to more edits. Conflict is defined by number of reverted articles normalized by total edits and article length. Other features include categories, diversity of references, type of reference, domain, number of edits done by bots. Currently conflictive articles in Wikipedia are manually protected by moderators when necessary. Future work will focus on automating the article protection in Wikipedia using machine learning.
Read further discussion [here](https://github.com/mv1742/Wiki_Bias/blob/master/Discussion.md). 

# 2. Motivation
- Wikipedia needs a metric to quantify the bias of its articles
- Understand behaviours in crowdsourcing platforms like Wikipedia
- Identify conflictive sources of information
- Evaluate quality of article references

# 3. Requirements
3.1 Data Ingestion
- Python3
- [AWS CLI](https://aws.amazon.com/cli/)
- [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#installation)

3.2 Data Processing
- Setup spark cluster
    - AWS (or alternative)  
        - AWS account
        - VPC with DNS Resolution enabled
        - Subnet in VPC
        - Security group accepting all inbound and outbound traffic
        - AWS Access Key ID and AWS Secret Access Key ID
- Spark packages
    - [Spark-XML](https://github.com/databricks/spark-xml)
    - [JDBC](https://jdbc.postgresql.org/download/postgresql-42.2.8.jar)

3.3 Database
- [Postgresql](https://www.postgresql.org/download/)
- [TimescaleDB](https://docs.timescale.com/latest/getting-started/installation)

3.4 Flask app
- [Requirements](.\src\flask\plotlydash-flask\requirements.txt)

# 4. Pipeline
![Pipeline.png](https://github.com/mv1742/Wiki_Bias/blob/master/figs/Pipeline.png)

# 5. Architecture
### Spark

6 EC2 m4.large instances (1 master 5 slaves spark cluster)

[Installation](https://blog.insightdatascience.com/simply-install-spark-cluster-mode-341843a52b88)

### Airflow

1 EC2 m4.xlarge instance

[Installation](https://blog.insightdatascience.com/scheduling-spark-jobs-with-airflow-4c66f3144660)

### PostgreSQL

1 EC2 m4.large instance

[Installation](https://blog.insightdatascience.com/simply-install-postgresql-58c1e4ebf252)

### Dash
1 EC2 m4.large instance

[Installation](https://dash.plot.ly/installation)

# 6. Data Source

~500 GB Wikipedia
Use English Wikipedia 'meta-stub' and 'meta-current' datadumps from [datadumps.wikipedia.org/enwiki]

Read more about the Wikipedia dump documentation [here](https://en.wikipedia.org/wiki/Wikipedia:Database_download).
See all available datasets [here](https://dumps.wikimedia.org/backup-index.html).


# 7. Metrics

    1. Article edit history
        1.1 Reverts
        1.2 Number of edits
        1.3 Username
        1.4 Timestamp
    2. Domain information
        2.1 Domain
        2.2 Url
        2.3 Title        
    3. Categories
        3.1 Infobox
        3.2 Sub-categories
    4. Other data
        4.1 Article length
        4.2 Number of links from article

# 8. Methodology
## 8.1 Data collection:
[generate_text_file.py](./src/ingestion/generate_text_file.py): 

- Uses the BeautifulSoup package to parse the urls on the stackexchange data dump to retrieve the urls of the .7z files of all the wikipedia dump

## 8.2 Parse Wikipedia articles
[articles.py](./src/dataprocessing/process_articles/articles.py): 

- Uses Regex and Spark to parse current Wikipedia articles 
- Extracts relevant features like references, name, categories, and article length


## 8.3 Parse Wikipedia edit history
[edit_history.py](./src/dataprocessing/process_articles/edit_history.py): 

- Uses Regex and Spark to parse historic Wikipedia meta-data 
- Extracts relevant features like edits, reverts, timestamp, and username

## 8.4 Run data analytics
[wiki_analytics.sql](./src/analytics/wiki_analytics.sql): 

- Uses SQL to calculate conflict score 
- Matches conflict score with different features using aggregations

[timeseries.sql](./src/analytics/timeseries.sql): 

- Uses SQL window functions to calculate rate of change per month, day, and year 
- Creates TimescaleDB partition to optimize query time

# 9. Getting started

Post installation of all the components of the pipeline, it can be used in two ways:
## 9.1 Initialize the DAG in Airflow and launch it on airflow scheduler:

` cp ~/Wiki_Bias/src/airflow/de_dag.py ~/airflow/de_dag.py`
 
` python3 de_dag.py`
  
## 9.2 Run the following scripts:

### 9.2.1 Data ingestion

` cd ~/Wiki_Bias/src/ingestion/`

`./download.sh`

### 9.2.2 Spark processing

` cd ~/Wiki_Bias/src/dataprocessing/`

`./run_articles.sh`

`./edit_history.sh`

### 9.2.3 SQL joins and analytics

`cd ~/Wiki_Bias/src/analytics`

`./run_analytics.sh`

### 9.2.4 Run Flask app

`cd ~/Wiki_Bias/src/flask`

`python3 wsgi.py`


# 10. Dashboard

![diagram](figs/db1.png)
__Figure 1.__ Dashboard showing time-series of the edit history

![diagram](figs/Month.png)
__Figure 2.__ Dashboard monthly top articles

![diagram](figs/db2.png)
__Figure 3.__ Dashboard overall top articles

![diagram](figs/db_3.png)
__Figure 4.__ Dashboard overall top domains

![diagram](figs/db3.png)
__Figure 5.__ Dashboard overall top categories

![diagram](figs/db4.png)
__Figure 6.__ Dashboard word cloud topic model

![diagram](figs/db_5.png)
__Figure 7.__ Search results

# 11. Analytics

## 11.1 Table schema
![diagram](figs/Schema.png)

# 12. Setup Notes

## 12.1. Spark to Postgresql

### 12.1.1 Setup JDBC

1. Download Postgresql jar file to Spark master node using `/Wiki_Bias/src/ingestion$ wget https://jdbc.postgresql.org/download/postgresql-42.2.8.jar`

2. Go to pg configuration using `sudo nano /etc/postgresql/10/main/pg_hba.conf` and update security to "md5":

    - local   all             all                                     md5

3. In postgresql.conf file, go to Connection Settings. Change the listening address to: listen_addresses = '*'

## 12.2 Spark tuning

Edit Spark configuration file /usr/local/spark/conf/spark-defaults.conf . See 
[how-to-tune-your-apache-spark-jobs-part-2](https://blog.cloudera.com/how-to-tune-your-apache-spark-jobs-part-2/) for more information. 
Below is a sample setup:

```
spark.driver.memory                4G 
spark.executor.memory              2G 
spark.driver.cores                 3 
spark.executor.cores               3
```

# 13. Repo directory structure

The directory structure looks like this:
```

├── README.md
├── figs
│   ├── Pipeline.png
│   ├── README.md
│   ├── db1.png
│   ├── db2.png
│   ├── db3.png
│   ├── db4.png
│   └── db5.png
└── src
    ├── airflow
    │   └── de_dag.py
    ├── analytics
    │   ├── run_analytics.sh
    │   └── wiki_analytics.sql
    ├── dataprocessing
    │   ├── README.md
    │   ├── merge
    │   │   └── merge.py
    │   ├── process_articles
    │   │   ├── README.md
    │   │   ├── articles.py
    │   │   └── run_articles.sh
    │   └── process_edit_history
    │       ├── README.md
    │       ├── edit_history.py
    │       └── run_edit_history.sh
    ├── flask
    │   ├── README.md
    │   ├── __init__.py
    │   ├── application
    │   ├── config.py
    │   ├── flask_app.py
    │   ├── ldacomplaints.py
    │   ├── requirements.txt
    │   ├── setup.py
    │   ├── start.sh
    │   └── wsgi.py
    └── ingestion
        ├── README.md
        ├── download.sh
        ├── generate_text_file.py
        └── text_files_download
            ├── enwiki_articles_multistream.txt
            └── enwiki_meta_history.txt

```

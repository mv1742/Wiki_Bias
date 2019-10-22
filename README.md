# Source of Conflict

![Python](https://img.shields.io/badge/Python-3.7-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![Flask](https://img.shields.io/badge/Flask-1.0.2-blue.svg?longCache=true&logo=flask&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![Flask-Assets](https://img.shields.io/badge/Flask--Assets-v0.12-blue.svg?longCache=true&logo=flask&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![Pandas](https://img.shields.io/badge/Pandas-v0.24.2-blue.svg?longCache=true&logo=python&longCache=true&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![Dash](https://img.shields.io/badge/Dash-v1.0.2-blue.svg?longCache=true&logo=python&longCache=true&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![Plotly](https://img.shields.io/badge/Plotly-v3.7.1-blue.svg?longCache=true&logo=python&longCache=true&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![Psycopg2-Binary](https://img.shields.io/badge/Psycopg2--Binary-v2.7.7-red.svg?longCache=true&style=flat-square&logo=PostgreSQL&logoColor=white&colorA=4c566a&colorB=bf616a)
![Flask-SQLAlchemy](https://img.shields.io/badge/Flask--SQLAlchemy-2.3.2-red.svg?longCache=true&style=flat-square&logo=scala&logoColor=white&colorA=4c566a&colorB=bf616a)

## Insight Data Engineering
## Manrique Vargas (MV), mv1742@nyu.edu

1. [Introduction](README.md#Report)
1. [Motivation](README.md#Motivation)
1. [Pipeline](README.md#Pipeline)
1. [Results](README.md#Results)
1. [Repo-directory-structure](README.md#Repo-directory-structure)


# Introduction
Source of Conflict is a tool to analyze how references and other features in Wikipedia articles affect the edit history. I calculate different metrics for bias and identify which metrics lead to more edits. Conflict is defined by number of reverted articles. Other features include categories, diversity of references, type of reference, domain, number of edits done by bots.

# Motivation
- Wikipedia needs a metric to quantify the bias of its articles.
- Understand behaviours in crowdsourcing platforms like Wikipedia
- Identify conflictive sources of information
- Evaluate quality of article references

# Pipeline
![Pipeline.png](https://github.com/mv1742/Wiki_Bias/blob/master/Images/Pipeline.png)

# Data Source
~500 GB Wikipedia
Use English Wikipedia 'meta-stub' and 'meta-current' datadumps from [datadumps.wikipedia.org/enwiki]

Read more about the Wikipedia dump documentation [here](https://en.wikipedia.org/wiki/Wikipedia:Database_download).
See all available datasets [here](https://dumps.wikimedia.org/backup-index.html).

# Results

Go to dashboard [dataangel.me](http://dataangel.me/8050).


## Repo directory structure

The directory structure looks like this:
```
├── README.md
└── src
    ├── Flask
    │   ├── Procfile
    │   ├── README.md
    │   ├── __pycache__
    │   │   └── ldacomplaints.cpython-36.pyc
    │   ├── app.py
    │   ├── app_mod.py
    │   ├── ldacomplaints.py
    │   ├── plotlydash-flask-tutorial
    │   ├── requirements.txt
    │   └── wordcloud_matplotlib.py
    ├── analytics
    │   ├── add_pageviews.sql
    │   └── wiki_analytics.sql
    ├── dataprocessing
    │   ├── README.md
    │   ├── export2postgres.py
    │   ├── merge
    │   │   └── merge.py
    │   ├── parse_xml.py
    │   ├── process_conflict.sql
    │   ├── process_refs
    │   │   ├── README.md
    │   │   ├── Single_ref.py
    │   │   ├── load_pickle.py
    │   └── process_reverts
    │       ├── Arts_revs.py
    │       ├── README.md
    │       ├── Single_rev.py
    │       └── run.sh
    └── ingestion
        ├── README.md
        ├── download.sh
        ├── generate_text_file.py
        └── text_files_download
            ├── enwiki_articles_multistream.txt
            └── enwiki_meta_history.txt
```

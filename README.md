# Source to Conflict

![Python](https://img.shields.io/badge/Python-3.7-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![Flask](https://img.shields.io/badge/Flask-1.0.2-blue.svg?longCache=true&logo=flask&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![Flask-Assets](https://img.shields.io/badge/Flask--Assets-v0.12-blue.svg?longCache=true&logo=flask&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![Pandas](https://img.shields.io/badge/Pandas-v0.24.2-blue.svg?longCache=true&logo=python&longCache=true&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![Dash](https://img.shields.io/badge/Dash-v1.0.2-blue.svg?longCache=true&logo=python&longCache=true&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![Plotly](https://img.shields.io/badge/Plotly-v3.7.1-blue.svg?longCache=true&logo=python&longCache=true&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![Psycopg2-Binary](https://img.shields.io/badge/Psycopg2--Binary-v2.7.7-red.svg?longCache=true&style=flat-square&logo=PostgreSQL&logoColor=white&colorA=4c566a&colorB=bf616a)
![Flask-SQLAlchemy](https://img.shields.io/badge/Flask--SQLAlchemy-2.3.2-red.svg?longCache=true&style=flat-square&logo=scala&logoColor=white&colorA=4c566a&colorB=bf616a)


1. [Introduction](README.md#Report)
1. [Repo-directory-structure](README.md#Repo-directory-structure)
1. [Motivation](README.md#Motivation)
1. [Pipeline](README.md#Pipeline)
1. [Results](README.md#Results)

# Introduction
Source to Conflict is a tool to quantify the quality in of references in Wikipedia articles. I calculate different metrics for bias and identify which metrics lead to more conflict. Conflict is defined by number of reverted articles. Other features include categories, diversity of references, type of reference, domain, number of edits done by bots.

# Motivation
- Wikipedia needs a metric to quantify the bias of its articles.
- Understand behaviours in crowdsourcing platforms like Wikipedia
- Identify conflictive sources of information
- Evaluate quality of article references

# Pipeline
![image](http://www.github.com/mv1742/Wiki_Bias/images/pipeline.jpeg)

# Data Source
~500 GB Wikipedia
Use English Wikipedia 'meta-stub' and 'meta-current' datadumps from [datadumps.wikipedia.org/enwiki]

Read more about the Wikipedia dump documentation [here](https://en.wikipedia.org/wiki/Wikipedia:Database_download).
See all available datasets [here](https://dumps.wikimedia.org/backup-index.html).

# Results

Go to dashboard [dataangel.me](http://dataangel.me).

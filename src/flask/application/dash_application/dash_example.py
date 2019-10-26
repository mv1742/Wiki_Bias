"""Create a Dash app within a flask app."""
from pathlib import Path
from dash import Dash
import dash_table
import dash_html_components as html
import pandas as pd
from .layout import html_layout
import os
import psycopg2
#os.environ["POSTGRES_HOSTNAME"] = sys.argv[1]
#os.environ["POSTGRES_USER"] = sys.argv[2]
#os.environ["POSTGRES_PASSWORD"] = sys.argv[3]
#os.environ["POSTGRES_DBNAME"] = sys.argv[4]


# user = os.environ["POSTGRES_USER"]
# host = os.environ["POSTGRES_HOSTNAME"]
# password = os.environ["POSTGRES_PASSWORD"]
# dbname = os.environ["POSTGRES_DBNAME"]
dbname='postgres'
host='ec2-3-222-98-195.compute-1.amazonaws.com'
user='postgres'
password='Sapr2019'
# export AWS_ACCESS_KEY_ID=AKIAZ4LCPHIH4IUQA5OB
# export AWS_SECRET_ACCESS_KEY=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
# export AWS_DEFAULT_REGION=us-east-1


# Settings for psycopg Postgres connector
con = psycopg2.connect(database=dbname, user=user, password=password, host=host)

# Monthly frequency of revisions
# sql_query_0 = "SELECT * FROM groupby_article_large_edits where entity_title is 'Via (Company)' ORDER BY reverts DESC LIMIT 50;"
sql_query_1 = "SELECT * FROM joined_distribution  where count_u is not null ORDER BY count_u DESC LIMIT 50;"
sql_query_2 = "SELECT ratio, title, url FROM s2conflict_urls_with_edit_history WHERE title is not null ORDER BY ratio DESC LIMIT 50;"
sql_query_3 = "SELECT * FROM source_score_ratio ORDER BY ratio_av DESC LIMIT 50;"
sql_query_4 = "SELECT * FROM source_score_reverts ORDER BY reverts_av DESC LIMIT 50;"
# sql_query_5 = "SELECT ratio, title, url FROM urls_article_title_all ORDER BY ratio DESC LIMIT 50;"
# Query result
dict_of_tables = {}
# dict_of_tables['0'] = pd.read_sql_query(sql_query_0, con)
dict_of_tables['1'] = pd.read_sql_query(sql_query_1, con)
dict_of_tables['2'] = pd.read_sql_query(sql_query_2, con)
dict_of_tables['3'] = pd.read_sql_query(sql_query_3, con)
dict_of_tables['4'] = pd.read_sql_query(sql_query_4, con)
# dict_of_tables['5'] = pd.read_sql_query(sql_query_5, con)


def Add_Dash(server):
    """Create a Dash app."""
    external_stylesheets = ['/static/dist/css/styles.css',
                            'https://fonts.googleapis.com/css?family=Lato',
                            'https://use.fontawesome.com/releases/v5.8.1/css/all.css']
    external_scripts = ['/static/dist/js/includes/jquery.min.js',
                        '/static/dist/js/main.js']
    dash_app = Dash(server=server,
                    external_stylesheets=external_stylesheets,
                    external_scripts=external_scripts,
                    routes_pathname_prefix='/dashapp/')

    # Override the underlying HTML template
    dash_app.index_string = html_layout

    # Create Dash Layout comprised of Data Tables
    dash_app.layout = html.Div(
        children=get_datasets(),
        id='dash-container'
      )

    return dash_app.server


def get_datasets():
    """Return previews of all CSVs saved in /data directory."""
    p = Path('.')
    data_filepath = list(p.glob('data/*.csv'))
    arr = ['This is an example Plot.ly Dash App.']
    for index, dataframe_pg in enumerate(dict_of_tables.values()):
        df = dataframe_pg.head(10)
        table_preview = dash_table.DataTable(
            id='table_' + str(index),
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("rows"),
            sort_action="native",
            sort_mode='single'
        )
        arr.append(table_preview)
    return arr

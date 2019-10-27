"""Create a Dash app within a flask app."""
from pathlib import Path
from dash import Dash
import dash_table
import dash_html_components as html
import pandas as pd
from .layout import html_layout
import os
import psycopg2


user = os.environ["POSTGRES_USER"]
host = os.environ["POSTGRES_HOSTNAME"]
password = os.environ["POSTGRES_PASSWORD"]
dbname = os.environ["POSTGRES_DBNAME"]

# Settings for psycopg Postgres connector
con = psycopg2.connect(database=dbname, user=user, password=password, host=host)

# Monthly frequency of revisions
sql_query_1 = "SELECT * FROM joined_distribution  where count_u is not null ORDER BY count_u DESC LIMIT 50;"
sql_query_2 = "SELECT ratio, title, url FROM s2conflict_urls_with_edit_history WHERE title is not null ORDER BY ratio DESC LIMIT 50;"
sql_query_3 = "SELECT * FROM source_score_ratio ORDER BY ratio_av DESC LIMIT 50;"
sql_query_4 = "SELECT * FROM source_score_reverts ORDER BY reverts_av DESC LIMIT 50;"
# Query result
dict_of_tables = {}
dict_of_tables['1'] = pd.read_sql_query(sql_query_1, con)
dict_of_tables['2'] = pd.read_sql_query(sql_query_2, con)
dict_of_tables['3'] = pd.read_sql_query(sql_query_3, con)
dict_of_tables['4'] = pd.read_sql_query(sql_query_4, con)


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

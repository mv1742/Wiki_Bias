import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
# import pandas_datareader.data as web
import plotly.graph_objs as go
from datetime import datetime
import pandas as pd
import numpy as np
import os
import flask
import psycopg2
from pathlib import Path
from dash import Dash
import time
from .layout import html_layout
import psycopg2
# user = os.environ["POSTGRES_USER"]
# host = os.environ["POSTGRES_HOSTNAME"]
# password = os.environ["POSTGRES_PASSWORD"]
# dbname = os.environ["POSTGRES_DBNAME"]
dbname='postgres'
host='ec2-3-222-98-195.compute-1.amazonaws.com'
# host = 'ec2-3-229-160-146.compute-1.amazonaws.com'
user='postgres'
password='Sapr2019'
# Settings for psycopg Postgres connector
con = psycopg2.connect(database=dbname, user=user, password=password, host=host)
#
# sql_query_1 = "SELECT host FROM groupby_url_ratio_relevant limit 100;"
# df = pd.read_sql_query(sql_query_1, con)
sql_query_1 = "SELECT * FROM source_score_ratio order by host_count desc limit 100;"
df = pd.read_sql_query(sql_query_1, con)
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
                    routes_pathname_prefix='/search/')
    dash_app.index_string = html_layout
    #--------------
    #---------------
    #--------------
    dash_app.layout = html.Div([
        html.H3('Loading State Example'),
        dcc.Dropdown(
            id='dropdown-search',
            options=[{'label': i, 'value': i} for i in list(df.host)]
        ),
        html.Div(id='output-search')
    ]+[html.Div(id="out-all-types")])

    @dash_app.callback(Output('output-search', 'children'), [Input('dropdown-search', 'value')])
    def update_value(value):
        # time.sleep(2)
        # print(df[df.host==value], df[df.host==value].rating.iloc[0], type(df[df.host==value].rating))

        return 'Domain {} has a conflict score of {}'.format(value, df[df.host==value].rating.iloc[0])
    return dash_app.server
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
import dash_table

from .layout import html_layout
import psycopg2
user = os.environ["POSTGRES_USER"]
host = os.environ["POSTGRES_HOSTNAME"]
password = os.environ["POSTGRES_PASSWORD"]
dbname = os.environ["POSTGRES_DBNAME"]

# Settings for psycopg Postgres connector


con = psycopg2.connect(database=dbname, user=user, password=password, host=host)

sql_query_boxplot = "SELECT * FROM url_media_query_conflictive_10 ORDER BY ratio DESC;"

# Query result
df_boxplot = pd.read_sql_query(sql_query_boxplot, con)
sql_query_histo = "SELECT reverts, title, host, nofedits, ratio FROM urls_article_title_relevant  where title is not null ORDER BY host LIMIT 25000;"
# Query result
df_histo = pd.read_sql_query(sql_query_histo, con)

sql_query_1_0= "SELECT * FROM groupby_article_large_edits WHERE ratio is not null ORDER BY nofedits DESC LIMIT 50;"
sql_query_1_1= "SELECT * FROM groupby_article_large_edits WHERE ratio is not null ORDER BY reverts DESC LIMIT 50;"
sql_query_1_2= "SELECT * FROM groupby_article_large_edits WHERE ratio is not null ORDER BY ratio DESC LIMIT 50;"

dict_of_tables = {}
data1_0 = pd.read_sql_query(sql_query_1_0,con)
data1_1 = pd.read_sql_query(sql_query_1_1,con)
data1_2 = pd.read_sql_query(sql_query_1_2,con)

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
                    routes_pathname_prefix='/articles/')
    dash_app.index_string = html_layout

    options = []

	# print('data0.head()', data1_1.head(25))

    dash_app.layout = html.Div([
		dcc.Markdown(''' --- '''),
		dcc.Markdown(''' --- '''),
		dcc.Markdown(''' --- '''),
		dcc.Markdown(''' --- '''),

		dcc.Markdown(''' \n\n\n '''),
		dcc.Markdown('''\n\n\n\n '''),
		html.H1('Analysis by Article'),
		# dcc.Markdown(''' --- '''),
		# Total Return Charts section
		# html.H1('Total Return Charts'),
		dcc.Graph(id='total23',
				  figure={'data': [
					  go.Bar(
						  x=data1_0['entity_title'][0:20],
						  y=data1_0['nofedits'][0:20],
						  name='Total number of edits'),
				  ],
					  'layout': go.Layout(title='Total Edits',
										  barmode='group',
										  xaxis={'automargin': True},
										  yaxis={'title': 'Edits Count'}
										  )}, style={'width': '100%'}
				  ),
		dcc.Markdown(''' --- '''),

		html.H1('Conflict Score and Reverts by Article'),
		dcc.Graph(id='ytd13', animate=True,
				  figure={'data': [
					  go.Bar(
						  x=data1_1['entity_title'][0:20],
						  y=data1_1['reverts'][0:20],
						  marker=dict(color='rgb(255, 144, 14)'),
						  name='Article Count'),
				  ],
					  'layout': go.Layout(title='Total Number of Reverts',
										  barmode='group',
										  xaxis={'automargin': True},
										  yaxis={'title': 'Reverts'},
										  # margin = {l=50,r=50,b=100,t=100,pad=4}
										  # yaxis = {'title':'host count', 'tickformat':".2%"}
										  )}, style={'width': '50%', 'display': 'inline-block', "margin": "auto"}
				  ),
		dcc.Graph(id='crot13',
				  figure={'data': [

					  go.Bar(
						  x=data1_2['entity_title'][0:20],
						  y=data1_2['ratio'][0:20],
						  marker=dict(color='rgb(8,81,156)'),
						  name='Conflict Score',
						  yaxis='y2')
				  ],
					  'layout': go.Layout(title='Conflict Score',
										  barmode='group',
										  xaxis={'automargin': True},
										  # xaxis = {'title': 'Conflict Score','automargin':True},
										  yaxis={'title': 'Conflict Score'},
										  )}, style={'width': '50%', 'display': 'inline-block', "margin": "auto"}
				  ),

		dcc.Markdown(''' --- '''),

	])
    return dash_app.server


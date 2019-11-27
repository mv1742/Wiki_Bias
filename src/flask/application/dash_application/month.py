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
from pathlib import Path
from dash import Dash
import time
from .layout import html_layout
import psycopg2

user = os.environ["POSTGRES_USER"]
host = os.environ["POSTGRES_HOSTNAME"]
password = os.environ["POSTGRES_PASSWORD"]
dbname = os.environ["POSTGRES_DBNAME"]

# Settings for psycopg Postgres connector


con = psycopg2.connect(database=dbname, user=user, password=password, host=host)

sql_query_1_0= "select * from rate_month_chunks where month = '2019-08-01' order by edits desc limit 10;"

dict_of_tables = {}
data1_0 = pd.read_sql_query(sql_query_1_0,con)

def Add_Dash(server):
	"""Create a Dash app."""
	# tickers = pd.DataFrame(data2.host.head(7))
	# tickers.set_index('host', inplace=True)
	external_stylesheets = ['/static/dist/css/styles.css',
							'https://fonts.googleapis.com/css?family=Lato',
							'https://use.fontawesome.com/releases/v5.8.1/css/all.css']
	external_scripts = ['/static/dist/js/includes/jquery.min.js',
						'/static/dist/js/main.js']
	dash_app = Dash(server=server,
					external_stylesheets=external_stylesheets,
					external_scripts=external_scripts,
					routes_pathname_prefix='/month/')
	dash_app.index_string = html_layout

	selected_dropdown_value = ['1/1/2015','2/1/2015','3/1/2015','4/1/2015','5/1/2015','6/1/2015','7/1/2015','8/1/2015','9/1/2015','10/1/2015','11/1/2015','12/1/2015','1/1/2016','2/1/2016','3/1/2016','4/1/2016','5/1/2016','6/1/2016','7/1/2016','8/1/2016','9/1/2016','10/1/2016','11/1/2016','12/1/2016','1/1/2017','2/1/2017','3/1/2017','4/1/2017','5/1/2017','6/1/2017','7/1/2017','8/1/2017','9/1/2017','10/1/2017','11/1/2017','12/1/2017','1/1/2018','2/1/2018','3/1/2018','4/1/2018','5/1/2018','6/1/2018','7/1/2018','8/1/2018','9/1/2018','10/1/2018','11/1/2018','12/1/2018','1/1/2019','2/1/2019','3/1/2019','4/1/2019','5/1/2019','6/1/2019','7/1/2019','8/1/2019']
	dropdown = '2019-08-01'
	trace1 = []
	sql_query_1_0= "select * from rate_month_chunks where month = '2019-08-01' order by reverts desc limit 10;"
	df = pd.read_sql_query(sql_query_1_0, con)
	df['Date'] = pd.to_datetime(df.month, infer_datetime_format=True, errors='ignore')
	df = df[df.Date.dt.year > 2003]
	df = df.sort_values(by='Date')
	trace1.append( go.Bar(
					  x=df['entity_title'],
					  y=df['reverts'],
					  name='Total number of reverts for month'+str(df['Date'][0])))
	traces = [trace1]
	data_ts = [val for sublist in traces for val in sublist]

	dash_app.layout = html.Div([html.H1("Analysis by Month", style={'textAlign': 'center'}),
								dcc.Dropdown(id='my-dropdown',
											 options=[{'label': key, 'value': key} for key in selected_dropdown_value],
											 style={"display": "block", "margin-left": "auto", "margin-right": "auto",
													"width": "60%"}),
								dcc.Graph(id='my-graph', figure={'data': data_ts,
																 'layout': go.Layout(
																	 colorway=["#5E0DAC", '#FF4F00', '#375CB1',
																			   '#FF7400', '#FFF400', '#FF0056'],
																	 height=600,
																	 title=f"Total reverts for month {dropdown}",
																	 barmode='group', xaxis={'automargin': True},
																	 yaxis={'title': 'Reverts Count'}
																	 )}, style={'width': '100%'}
				  ),
								], className="container")

	@dash_app.callback(Output('my-graph', 'figure'),
					   [Input('my-dropdown', 'value')])
	def update_graph(selected_dropdown_val):
		print(selected_dropdown_value)
		# sql_query_1_0 = "select * from rate_month where month = '2019-08-01' order by reerts desc limit 10;"
		sql_query_1 = "select * from rate_month_chunks where month = '"+ str(selected_dropdown_val) +"' order by reverts desc limit 10;"
		print(sql_query_1)
		df = pd.read_sql_query(sql_query_1, con)
		df['Date'] = pd.to_datetime(df.month, infer_datetime_format=True, errors='ignore')
		trace2 = []
		trace2.append(go.Bar(
			x=df['entity_title'],
			y=df['reverts'],
			name='Total number of reverts for month' + str(df['Date'][0])))

		traces = [trace2]
		data_ts = [val for sublist in traces for val in sublist]
		figure = {'data': data_ts,
				  'layout': go.Layout(
					  colorway=["#5E0DAC", '#FF4F00', '#375CB1',
								'#FF7400', '#FFF400', '#FF0056'],
					  height=600,
					  title=f"Total reverts for month {selected_dropdown_val}",
					  barmode='group', xaxis={'automargin': True},
					  yaxis={'title': 'Revert Count'}
				  )}
		return figure
	return dash_app.server


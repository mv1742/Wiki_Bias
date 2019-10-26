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

dbname='postgres'
host='ec2-3-222-98-195.compute-1.amazonaws.com'
user='postgres'
password='Sapr2019'


con = psycopg2.connect(database=dbname, user=user, password=password, host=host)

# Query result

def update_figure_boxplot():
    traces = []
    sql_query_2 = "SELECT * FROM Groupby_infobox_count_id_relevant_lb4  WHERE count is not null ORDER BY count DESC LIMIT 200;"
    data2 = pd.read_sql_query(sql_query_2, con)


    sql_query_boxplot = "SELECT * FROM groupby_id_infobox where ratio_av is not null;"
    dff = pd.read_sql_query(sql_query_boxplot, con)

    for host in data2.infobox.unique()[:8]:
        print(host,dff[dff["infobox"] == host])
        # dff[dff["host"] == host]["ratio"]
        traces.append(go.Box(y=dff[dff["infobox"] == host]["ratio_av"],name=host,marker={"size": 4}))
    return {"data": traces,
            "layout": go.Layout(title=f"Conflict Score for top 6 categories",autosize=True,
                                xaxis={'automargin': True},
                                # margin={"l": 200, "b": 100, "r": 200},xaxis={"showticklabels": False,},
                                yaxis={"title": f"Conflict Score","type": "log",},)}
def update_figure_boxplot2():
    # dff = df_boxplot
    traces = []
    sql_query_2 = "SELECT * FROM Groupby_infobox_count_id_relevant_lb5  WHERE count is not null LIMIT 200;"
    data2 = pd.read_sql_query(sql_query_2, con)


    sql_query_boxplot = "SELECT * FROM groupby_id_infobox where ratio_av is not null;"
    dff = pd.read_sql_query(sql_query_boxplot, con)
    for host in data2.infobox.unique()[:8]:
        print(host,dff[dff["infobox"] == host])
        # dff[dff["host"] == host]["ratio"]
        traces.append(go.Box(y=dff[dff["infobox"] == host]["ratio_av"],name=host,marker={"size": 4}))
    return {"data": traces,
            "layout": go.Layout(title=f"Conflict Score for top 6 categories",autosize=True,
                                xaxis={'automargin': True},
                                showlegend=False,
                                # margin={"l": 200, "b": 100, "r": 200},xaxis={"showticklabels": False,},
                                yaxis={"title": f"Conflict Score","type": "log",},)}

def update_figure_boxplot3():
    # dff = df_boxplot
    traces = []
    sql_query_2 = "SELECT * FROM Groupby_infobox_count_id_relevant_lb5  WHERE count is not null ORDER BY count DESC LIMIT 200;"
    data2 = pd.read_sql_query(sql_query_2, con)


    sql_query_boxplot = "SELECT * FROM groupby_id_infobox where ratio_av is not null;"
    dff = pd.read_sql_query(sql_query_boxplot, con)

    for host in data2.infobox.unique()[:100]:
        print(host,dff[dff["infobox"] == host])
        # dff[dff["host"] == host]["ratio"]
        traces.append(go.Box(y=dff[dff["infobox"] == host]["ratio_av"],name=host,marker={"size": 4}))
    return {"data": traces,
            "layout": go.Layout(title=f"Conflict Score for Top 8 Categories",autosize=True,
                                xaxis={'automargin': True},
                                # margin={"l": 200, "b": 100, "r": 200},xaxis={"showticklabels": False,},
                                yaxis={"title": f"Conflict Score","type": "log",},)}

sql_query_1_0= "SELECT * FROM Groupby_len_relevant WHERE ratio_av is not null ORDER BY nofedits_av DESC LIMIT 50;"
sql_query_1_1= "SELECT * FROM Groupby_len_relevant WHERE ratio_av is not null ORDER BY reverts_av DESC LIMIT 50;"
sql_query_1_2= "SELECT * FROM Groupby_len_relevant WHERE ratio_av is not null ORDER BY ratio_av DESC LIMIT 50;"
sql_query_2 = "SELECT * FROM Groupby_infobox_count_id_relevant_lb5  WHERE count is not null ORDER BY reverts_av DESC LIMIT 200;"
sql_query_3 = "SELECT * FROM Groupby_infobox_count_id_relevant_lb5  where count is not null ORDER BY ratio_av DESC LIMIT 200;"
dict_of_tables = {}

data2 = pd.read_sql_query(sql_query_2, con)
data2 = data2.groupby('infobox').mean()
# print(dff.head())

data2.sort_values('reverts_av', ascending=False, inplace=True)
data2.reset_index(inplace=True)
data3 = pd.read_sql_query(sql_query_3, con)
data3 = data3.groupby('infobox').mean()
# print(dff.head())
data3.sort_values('ratio_av', ascending=False, inplace=True)
data3.reset_index(inplace=True)
# data3.sort_values('ratio_av', inplace=True)
def Add_Dash(server):
    """Create a Dash app."""
    tickers = pd.DataFrame(data2.infobox.head(7))
    tickers.set_index('infobox', inplace=True)
    external_stylesheets = ['/static/dist/css/styles.css',
                            'https://fonts.googleapis.com/css?family=Lato',
                            'https://use.fontawesome.com/releases/v5.8.1/css/all.css']
    external_scripts = ['/static/dist/js/includes/jquery.min.js',
                        '/static/dist/js/main.js']
    dash_app = Dash(server=server,
                    external_stylesheets=external_stylesheets,
                    external_scripts=external_scripts,
                    routes_pathname_prefix='/categories/')
    dash_app.index_string = html_layout

    options = []
    for tic in tickers.index:
        mydict = {}
        mydict['label'] = tic  # Apple Co. AAPL
        mydict['value'] = tic
        options.append(mydict)

    dash_app.layout = html.Div([

        dcc.Markdown(''' \n --- \n '''),
        dcc.Markdown('''\n\n\n\n '''),
        dcc.Markdown('''  '''),
        dcc.Markdown(''' --- '''),
        dcc.Markdown(''' --- '''),
        dcc.Markdown(''' --- '''),

        # Total Return Charts section
        html.H1('\n\n\n Analysis by Category'),
        dcc.Graph(id='total1',
                  figure={'data': [
                      go.Bar(
                          x=data2['infobox'][:20],
                          y=data2['reverts_av'][:20],
                          marker=dict(color='rgb(255, 144, 14)'),
                          name='Average Reverts by Category'),
                  ],
                      'layout': go.Layout(title='Average Reverts',
                                          barmode='group',
                                          xaxis={'automargin': True},
                                          yaxis={'title': 'Reverts'}
                                          )}, style={'width': '50%', 'display': 'inline-block'}
                  ),
        dcc.Graph(id='crot2',
				  figure={'data': [go.Bar(
						  x=data3['infobox'][1:20],
						  y=data3['ratio_av'][1:20],
						  name='Average Conflict Score per Category'),

				  ],
					  'layout': go.Layout(title='Average Conflict Score per Category',
										  barmode='group',
										  xaxis={'automargin': True},
										  yaxis={'title': 'Conflict Score'},
										  )}, style={'width': '50%', 'display': 'inline-block', "margin": "auto"}
				  ),
        dcc.Markdown(''' --- '''),


        html.H1("Conflict Score Distribution for Top Categories"),
        dcc.Graph(id="my-graph2", figure=update_figure_boxplot2()),


    ])
    return dash_app.server


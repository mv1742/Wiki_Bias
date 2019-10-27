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

sql_query_boxplot = "SELECT host FROM url_media_query_conflictive_100 ORDER BY ratio DESC;"

# Query result
df_boxplot = pd.read_sql_query(sql_query_boxplot, con)
sql_query_histo = "SELECT reverts, title, host, nofedits, ratio FROM urls_article_title_relevant  where title is not null ORDER BY host LIMIT 25000;"

# Query result
df_histo = pd.read_sql_query(sql_query_histo, con)

def update_graph_histo():

    trace = go.Histogram(x=df_histo.ratio.to_numpy())
    layout = go.Layout(title=f"Conflict Score Distribution", xaxis={"title": "Ratio", "showgrid": False},
                       yaxis={"title": "Count", "showgrid": False},)
    figure2 = {"data": [trace], "layout": layout}#style:{'width': '50%', 'display': 'inline-block', "margin": "auto"}}
    return figure2


# Year,Country,Continent,Emission
def update_figure_boxplot3():
    # dff = df_boxplot
    traces = []
    sql_query_boxplot = "SELECT host FROM source_score_ratio order by host_count desc limit 10;"
    dff = pd.read_sql_query(sql_query_boxplot, con)
    for host in dff.host.unique()[:8]:
        sql_query_boxplot = "SELECT * FROM url_media_query_top_news where host = \'"+host+"\' limit 2000;"
        dff = pd.read_sql_query(sql_query_boxplot, con)

        traces.append(go.Box(y=dff[dff["host"] == host]["ratio"], name=host, marker={"size": 4}))
    return {"data": traces,
            "layout": go.Layout(title=f"Conflict Score for 8 Most Cited Domains in English Wikipedia", autosize=True,
                                xaxis={'automargin': True},
                                # margin={"l": 200, "b": 100, "r": 200},xaxis={"showticklabels": False,},
                                yaxis={"title": f"Conflict Score", "type": "log", }, )}
def update_figure_boxplot2():
    dff = df_boxplot
    traces = []
    for host in dff.host.unique():
        sql_query_boxplot2 = "SELECT * FROM url_media_query_conflictive_10 where host =\'"+str(host)+"\' ORDER BY ratio DESC;"
        # print(sql_query_boxplot2)
        dff_2 = pd.read_sql_query(sql_query_boxplot2, con)
        traces.append(go.Box(y=dff_2[dff_2["host"] == host]["ratio"],name=host,marker={"size": 4}))
    return {"data": traces,
            "layout": go.Layout(title=f"Conflict Score for 8 Popular Domains in United States",autosize=True,
                                xaxis={'automargin': True},
                                # margin={"l": 200, "b": 100, "r": 200},xaxis={"showticklabels": False,},
                                yaxis={"title": f"Conflict Score","type": "log",},)}

sql_query_2 = "SELECT * FROM source_score_reverts WHERE host is not null ORDER BY reverts_av DESC LIMIT 50;"
sql_query_2_1 = "SELECT * FROM source_score_reverts WHERE host is not null ORDER BY host_count DESC LIMIT 50;"


sql_query_3 = "SELECT * FROM source_score_ratio ORDER BY ratio_av DESC LIMIT 50;"
sql_query_3_1 = "SELECT * FROM source_score_ratio ORDER BY host_count DESC LIMIT 50;"

dict_of_tables = {}
data2 = pd.read_sql_query(sql_query_2, con)
data2_1 = pd.read_sql_query(sql_query_2_1, con)
data3 = pd.read_sql_query(sql_query_3, con)
data3_1 = pd.read_sql_query(sql_query_3_1, con)

def Add_Dash(server):
    """Create a Dash app."""
    tickers = pd.DataFrame(data2.host.head(7))
    tickers.set_index('host', inplace=True)
    external_stylesheets = ['/static/dist/css/styles.css',
                            'https://fonts.googleapis.com/css?family=Lato',
                            'https://use.fontawesome.com/releases/v5.8.1/css/all.css']
    external_scripts = ['/static/dist/js/includes/jquery.min.js',
                        '/static/dist/js/main.js']
    dash_app = Dash(server=server,
                    external_stylesheets=external_stylesheets,
                    external_scripts=external_scripts,
                    routes_pathname_prefix='/analytics/')
    dash_app.index_string = html_layout

    options = []
    for tic in tickers.index:
        mydict = {}
        mydict['label'] = tic  # Apple Co. AAPL
        mydict['value'] = tic
        options.append(mydict)


    dash_app.layout = html.Div([		dcc.Markdown('''\n\n---\n\n '''),
                                        dcc.Markdown(''' --- '''),
                                        dcc.Markdown(''' --- '''),
                                        dcc.Markdown(''' --- '''),

                                        html.H1('Analysis by Domain'),
                                        dcc.Graph(id='ytd1', animate=True,
                                                  figure={'data': [
                                                      go.Bar(
                                                          x=data2_1['host'][0:20],
                                                          y=data2_1['host_count'][0:20],
                                                          name='Host count'),
                                                  ],
                                                      'layout': go.Layout(title='Citations per Domain',
                                                                          barmode='group',
                                                                          xaxis={'automargin': True},
                                                                          yaxis={'title': 'Domain reverts'},
                                                                          )},
                                                  ),
        dcc.Graph(id='crot2',
                  figure={'data': [

                      go.Bar(
                          x=data3['host'][0:20],
                          y=data3['ratio_av'][0:20],
                          marker=dict(color='rgb(255, 144, 14)'),
                          name='Average Conflict Score per Domain'),

                  ],
                      'layout': go.Layout(title='Conflict Score per Domain',
                                          barmode='group',
                                          xaxis={'automargin': True},
                                          yaxis={'title': 'Conflict Score'},
                                          )}, style={'width': '50%', 'display': 'inline-block', "margin": "auto"}
                  ),

        dcc.Graph(id='total1',
                  figure={'data': [
                      go.Bar(
                          x=data2['host'][0:20],
                          y=data2['reverts_av'][0:20],
                          marker=dict(color='rgb(8,81,156)'),
                          name='Average Reverts per Domain'),
                  ],
                      'layout': go.Layout(title='Average Reverts',
                                          barmode='group',
                                          xaxis={'automargin': True},
                                          yaxis={'title': 'Reverts'}
                                          )}, style={'width': '50%', 'display': 'inline-block'}
                  ),


        dcc.Markdown(''' --- '''),


        html.H1("Score distribution for main media channels"),
                           dcc.Graph(id="my-graph", figure=update_figure_boxplot2()),
        dcc.Graph(id="hist-graph", figure=update_graph_histo()),

    ])
    return dash_app.server


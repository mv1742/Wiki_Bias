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
user = os.environ["POSTGRES_USER"]
host = os.environ["POSTGRES_HOSTNAME"]
password = os.environ["POSTGRES_PASSWORD"]
dbname = os.environ["POSTGRES_DBNAME"]


# Settings for psycopg Postgres connector
con = psycopg2.connect(database=dbname, user=user, password=password, host=host)
sql_query_2= "SELECT * FROM groupby_article_large_edits limit 50;"
df2 = pd.read_sql_query(sql_query_2, con)
dict_df2 = {}
for index, row in df2.iterrows():
    dict_df2[row['id']]=row['entity_title']

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
                    routes_pathname_prefix='/timeseries/')
    dash_app.index_string = html_layout
    selected_dropdown_value = [41688778,52644751,61008894] #  13404: "Hong Kong",43971623: "Hong Kong Protests 2014",61008894: "Hong Kong Protests 2019",

    dropdown = {41688778: " Brexit",  52644751 : "Efforts to impeach Donald Trump",61008894:"2019 Hong Kong protests"}
    trace1 = []
    trace2 = []
    trace3 = []
    for stock in selected_dropdown_value:
        sql_query_2_3 = "SELECT * FROM timescale_ts22 where entity_id = "+str(stock)+";"
        df = pd.read_sql_query(sql_query_2_3, con)
        df['edits'] = 1
        df['Date'] = pd.to_datetime(df.date_holder, infer_datetime_format=True, errors='ignore')
        df = df[df.Date.dt.year > 2003]
        # df = df[df.Date.dt.year < 2019]
        df = df.sort_values(by='Date')
        trace1.append(
            go.Scatter(x=df[df["entity_id"] == stock]["Date"], y=df[df["entity_id"] == stock].reverts_ind.cumsum(),
                       mode='lines',
                       opacity=0.7, name=f'Reverts {dropdown[stock]}', textposition='bottom center')),
        trace2.append(
            go.Scatter(x=df[df["entity_id"] == stock]["Date"], y=df[df["entity_id"] == stock].bots_ind.cumsum(),
                       mode='lines',
                       opacity=0.6, name=f'Bots {dropdown[stock]}', textposition='bottom center')),
        trace3.append(
            go.Scatter(x=df[df["entity_id"] == stock]["Date"], y=df[df["entity_id"] == stock].edits.cumsum(),
                       mode='lines',
                       opacity=0.6, name=f'Edits {dropdown[stock]}', textposition='bottom center')),
    traces = [trace1]#, trace2, trace3]
    data_ts = [val for sublist in traces for val in sublist]
    dash_app.layout = html.Div([html.H1("Revert History", style={'textAlign': 'center'}),
                           dcc.Dropdown(id='my-dropdown', options=[{'label': val, 'value': key} for key,val in dict_df2.items()],
                                        # multi=True, value=['8209'],
                                        style={"display": "block", "margin-left": "auto", "margin-right": "auto",
                                               "width": "60%"}),
                           dcc.Graph(id='my-graph',figure = {'data': data_ts,
              'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                                  height=600,
                                  title=f"Reverts for {', '.join(str(dropdown[i]) for i in selected_dropdown_value)} Over Time",
                                  xaxis={"title": "Date",
                                         'rangeselector': {'buttons': list(
                                             [{'count': 6, 'label': '6Y', 'step': 'year', 'stepmode': 'backward'},
                                              {'count': 12, 'label': '12Y', 'step': 'year', 'stepmode': 'backward'},
                                              {'step': 'all'}])},
                                         'rangeslider': {'visible': True}, 'type': 'date'},
                                  yaxis={"title": "Edit type"})})
                           ], className="container")


    @dash_app.callback(Output('my-graph', 'figure'),
                       [Input('my-dropdown', 'value')])
    def update_graph(selected_dropdown_value):

        print(selected_dropdown_value)
        sql_query_1 = "SELECT * FROM timescale_ts22 where entity_id = "+str(selected_dropdown_value)+";"
        df = pd.read_sql_query(sql_query_1, con)
        df['edits'] = 1
        df['Date'] = pd.to_datetime(df.date_holder, infer_datetime_format=True, errors='ignore')
        df = df[df.Date.dt.year > 2003]
        df = df[df.Date.dt.year < 2018]
        df = df.sort_values(by='Date')

        trace1 = go.Scatter(x=df[df["entity_id"] == selected_dropdown_value]["Date"], y=df[df["entity_id"] == selected_dropdown_value].reverts_ind.cumsum(),
                       mode='lines',
                       opacity=0.7, name=f'Reverts {dict_df2[selected_dropdown_value]}', textposition='bottom center'),
        trace2 = go.Scatter(x=df[df["entity_id"] == selected_dropdown_value]["Date"], y=df[df["entity_id"] == selected_dropdown_value].bots_ind.cumsum(),
                           mode='lines',
                           opacity=0.6, name=f'Bots {dict_df2[selected_dropdown_value]}', textposition='bottom center'),
        trace3 = go.Scatter(x=df[df["entity_id"] == selected_dropdown_value]["Date"], y=df[df["entity_id"] == selected_dropdown_value].edits.cumsum(),
                           mode='lines',
                           opacity=0.6, name=f'Edits {dict_df2[selected_dropdown_value]}', textposition='bottom center'),
        traces = [trace1,trace2,trace3]
        data_ts = [val for sublist in traces for val in sublist]
        figure = {'data': data_ts,
                  'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                                      height=600,title=f"Reverts and bots for {dict_df2[selected_dropdown_value]} Over Time",
                                      # title=f"Edits, reverts, and bots for {', '.join(str(dropdown[i]) for i in selected_dropdown_value)} Over Time",
                                      xaxis={"title": "Date",
                                             'rangeselector': {'buttons': list(
                                                 [{'count':6, 'label': '6Y', 'step': 'year', 'stepmode': 'backward'},
                                                  {'count': 12, 'label': '12Y', 'step': 'year', 'stepmode': 'backward'},
                                                  {'step': 'all'}])},
                                             'rangeslider': {'visible': True}, 'type': 'date'},
                                      yaxis={"title": "Edit type"})}
        return figure

    return dash_app.server

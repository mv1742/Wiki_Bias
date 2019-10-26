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
# import dash_html_components as html
# import pandas as pd
# from .layout import html_layout
# import oss
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
# sql_query_4 = "SELECT * FROM source_score_reverts ORDER BY reverts_av DESC LIMIT 1000;"
# sql_query_5 = "SELECT * FROM urls_article_all ORDER BY reverts DESC LIMIT 2000;"
# Query result

# dict_of_tables['5'] = pd.read_sql_query(sql_query_5, con)
# sql_query_histo = "SELECT reverts_av, title, host, nofedits, ratio FROM urls_article_title_relevant  where title is not null ORDER BY host LIMIT 25000;"
# Query result
# df_histo = pd.read_sql_query(sql_query_histo, con)

# # def update_graph_histo():
#     dff = df
#     print(df.head(50))
    # trace = go.Histogram(x=df_histo.ratio.to_numpy())
    # layout = go.Layout(title=f"Ratio Distribution (sources with number of citations more than one std above the mean)", xaxis={"title": "Ratio", "showgrid": False},
    #                    yaxis={"title": "Count", "showgrid": False}, )
    # figure2 = {"data": [trace], "layout": layout}#style:{'width': '50%', 'display': 'inline-block', "margin": "auto"}}
    # return figure2


# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/Emissions%20Data.csv')
# Year,Country,Continent,Emission

def update_figure_boxplot():
    # dff = df_boxplot
    traces = []
    sql_query_2 = "SELECT * FROM Groupby_infobox_count_id_relevant_lb4  WHERE count is not null ORDER BY count DESC LIMIT 200;"
    data2 = pd.read_sql_query(sql_query_2, con)


    sql_query_boxplot = "SELECT * FROM groupby_id_infobox where ratio_av is not null;"
    dff = pd.read_sql_query(sql_query_boxplot, con)
    # print(dff.head())
    # dff.sort_values('reverts_av', ascending=False, inplace=True)
    # dff.reset_index(inplace=True)
    # print(dff.infobox.unique())
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
    # print(dff.head())
    # dff.sort_values('reverts_av', ascending=False, inplace=True)
    # dff.reset_index(inplace=True)
    # print(dff.infobox.unique())
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
    # print(dff.head())
    # dff.sort_values('reverts_av', ascending=False, inplace=True)
    # dff.reset_index(inplace=True)
    # print(dff.infobox.unique())
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
# data1_0 = pd.read_sql_query(sql_query_1_0,con)
# data1_1 = pd.read_sql_query(sql_query_1_1,con)
# data1_2 = pd.read_sql_query(sql_query_1_2,con)
data2 = pd.read_sql_query(sql_query_2, con)
data2 = data2.groupby('infobox').mean()
# print(dff.head())

data2.sort_values('reverts_av', ascending=False, inplace=True)
data2.reset_index(inplace=True)
# data2.sort_values('reverts_av',inplace=True)
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
        # html.H1('Reverts Analysis by Category'),
        # dcc.Graph(id='ytd1', animate=True,
        # 		  figure={'data': [
        # 			  go.Bar(
        # 				  x=data2['infobox'][0:20],
        # 				  y=data2['count'][0:20],
        # 				  name='Infobox count',)
        # 		  ],
        # 			  'layout': go.Layout(title='Total Number of Reverts by Infobox',
        # 								  barmode='group',
        # 								  xaxis={'automargin': True},
        # 								  yaxis={'title': 'Infobox'},
        # 								  # margin = {l=50,r=50,b=100,t=100,pad=4}
        # 								  # yaxis = {'title':'host count', 'tickformat':".2%"}
        # 								  )}, style={'width': '50%', 'display': 'inline-block', "margin": "auto"}
        # 		  ),
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
				  figure={'data': [
					  # go.Bar(
					  # x = data3['host'][0:20],
					  # y = data3['rating'][0:20],
					  # name = 'Host Rating'),
					  go.Bar(
						  x=data3['infobox'][1:20],
						  y=data3['ratio_av'][1:20],
						  name='Average Conflict Score per Category'),
					  # go.Bar(
					  # x = data3['host'][0:20],
					  # y = data3['host_count'][0:20],
					  # name = 'host_count %',
					  # yaxis='y2')
				  ],
					  'layout': go.Layout(title='Average Conflict Score per Category',
										  barmode='group',
										  xaxis={'automargin': True},
										  yaxis={'title': 'Conflict Score'},
										  )}, style={'width': '50%', 'display': 'inline-block', "margin": "auto"}
				  ),

        dcc.Markdown(''' --- '''),

        # Cumulative Returns Over Time section
       # dcc.Graph(id='crot1',
        # 		  figure={'data': [
        # 			  # go.Bar(
        # 			  # x = data3['host'][0:20],
        # 			  # y = data3['rating'][0:20],
        # 			  # name = 'Host Rating'),
        # 			  # go.Bar(
        # 			  # x = data3['host'][0:20],
        # 			  # y = data3['ratio_av'][0:20],
        # 			  # name = 'Average Ratio'),
        # 			  go.Bar(
        # 				  x=data3['infobox'][0:20],
        # 				  y=data3['count'][0:20],
        # 				  name='Infobox count'),
        # 			  # yaxis='y2')
        # 		  ],
        # 			  'layout': go.Layout(title='Total Length',
        # 								  barmode='group',
        # 								  xaxis={'automargin': True},
        # 								  # xaxis = {'title': 'host','automargin':True},
        # 								  yaxis={'title': 'Ratio (Reverts/(Total Number of Edits))'},
        # 								  yaxis2={'title': 'Total count', 'automargin': True, 'overlaying': 'y',
        # 										  'side': 'right', 'tickformat': ".1%"},
        # 								  )}, style={'width': '50%', 'display': 'inline-block', "margin": "auto"}
        # 		  ),


        # html.H1('Analysis per Article Length'),
        # # dcc.Markdown(''' --- '''),
        # # Total Return Charts section
        # # html.H1('Total Return Charts'),
        # dcc.Graph(id='total23',
        # 		  figure={'data': [
        # 			  go.Bar(
        # 				  x=data1_0['len_text'][0:20],
        # 				  y=data1_0['nofedits_av'][0:20],
        # 				  name='Total number of edits'),
        # 		  ],
        # 			  'layout': go.Layout(title='Total Edits',
        # 								  barmode='group',
        # 								  xaxis={'automargin': True},
        # 								  yaxis={'title': 'Edits Count'}
        # 								  )}, style={'width': '100%'}
        # 		  ),
        # dcc.Markdown(''' --- '''),
        #
        # html.H1('Ratio and Reverts by Article Length'),
        # dcc.Graph(id='ytd13', animate=True,
        # 		  figure={'data': [
        # 			  go.Bar(
        # 				  x=data1_1['len_text'][0:20],
        # 				  y=data1_1['reverts_av'][0:20],
        # 				  name='Article Count'),
        # 		  ],
        # 			  'layout': go.Layout(title='Total Number of Reverts',
        # 								  barmode='group',
        # 								  xaxis={'automargin': True},
        # 								  yaxis={'title': 'Reverts'},
        # 								  # margin = {l=50,r=50,b=100,t=100,pad=4}
        # 								  # yaxis = {'title':'host count', 'tickformat':".2%"}
        # 								  )}, style={'width': '50%', 'display': 'inline-block', "margin": "auto"}
        # 		  ),
        # dcc.Graph(id='crot13',
        # 		  figure={'data': [
        # 			  # go.Bar(
        # 			  # x = data3['host'][0:20],
        # 			  # y = data3['rating'][0:20],
        # 			  # name = 'Host Rating'),
        # 			  # go.Bar(
        # 			  # x = data3['host'][0:20],
        # 			  # y = data3['ratio_av'][0:20],
        # 			  # name = 'Average Ratio'),
        # 			  go.Bar(
        # 				  x=data1_2['len_text'][0:20],
        # 				  y=data1_2['ratio_av'][0:20],
        # 				  name='Ratio',
        # 				  yaxis='y2')
        # 		  ],
        # 			  'layout': go.Layout(title='Ratio (Reverts/(Total Number of Edits))',
        # 								  barmode='group',
        # 								  xaxis={'automargin': True},
        # 								  # xaxis = {'title': 'host','automargin':True},
        # 								  yaxis={'title': 'Ratio'},
        # 								  )}, style={'width': '50%', 'display': 'inline-block', "margin": "auto"}
        # 		  ),
        #
        html.H1("Conflict Score Distribution for Top Categories"),
                           # dcc.Graph(id="my-graph", figure=update_figure_boxplot()),
        dcc.Graph(id="my-graph2", figure=update_figure_boxplot2()),
        # dcc.Graph(id="my-graph3", figure=update_figure_boxplot3()),

        # dcc.Graph(id="hist-graph", figure=update_graph_histo()),

    ])
    return dash_app.server


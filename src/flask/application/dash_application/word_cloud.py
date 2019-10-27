# -*- coding: utf-8 -*-
import flask
import dash
import pathlib
import matplotlib.colors as mcolors
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objs as go
from dash.dependencies import Output, Input, State
from datetime import datetime
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import re
from ldacomplaints import lda_analysis
import psycopg2
import os
from pathlib import Path
import dash_table
import dash_html_components as html
import pandas as pd
from .layout import html_layout
from dash import Dash
user = os.environ["POSTGRES_USER"]
host = os.environ["POSTGRES_HOSTNAME"]
password = os.environ["POSTGRES_PASSWORD"]
dbname = os.environ["POSTGRES_DBNAME"]

# Settings for psycopg Postgres connector
con = psycopg2.connect(database=dbname, user=user, password=password, host=host)


# Query result
dict_of_tables = {}
DATA_PATH = pathlib.Path(__file__).parent.resolve()

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
filename = "customer_complaints_narrative_sample.csv"

"""
#  Helpful functions
"""
def load_data():
    print("loading data...")
    sql_query_boxplot = "SELECT host,host_count FROM source_score_ratio order by host_count desc LIMIT 200;"
    dff = pd.read_sql_query(sql_query_boxplot, con)
    dff = dff.dropna()
    dff = dff.rename(
        columns={'ratio_av': 'Date received', 'host': 'Company'})
    print('-----------------------\n\n\n\n',dff.head())
    return dff
def load_data_all(selected_bank):
    print("loading data...done")
    sql_query_5 = "SELECT ratio, title, host FROM urls_article_title_all where host = \'" + selected_bank + "\' and title is not null ORDER BY reverts DESC limit 200;"
    print(sql_query_5)
    dict_of_tables['5'] = pd.read_sql_query(sql_query_5, con)
    df_tables = dict_of_tables['5'].rename(
        columns={'ratio': 'Date received', 'title': 'Consumer complaint narrative', 'host': 'Company'})
    print(df_tables.head())
    print("loading data...done!")
    return df_tables

def sample_data(dataframe, float_percent):
    return dataframe.sample(frac=float_percent, random_state=1)


def crunch_data(dataframe):
    companyCounts = dataframe["Company"].value_counts()
    values = companyCounts.keys().tolist()
    counts = companyCounts.tolist()
    companyCounts_sample = companyCounts[:sample_size]
    values_sample = companyCounts_sample.keys().tolist()
    counts_sample = companyCounts_sample.tolist()


def calculate_full(dataframe):
    print(dataframe.head())
    companyCounts = dataframe["Company"].value_counts()
    values = companyCounts.keys().tolist()
    counts = companyCounts.tolist()
    print('dropdown----------------------',values,counts)
    return values, counts


def calculate_sample(dataframe, sample_size, time_values):
    print("got:", str(time_values))
    dataframe["Date received"]



    if time_values is not None:
        dataframe = dataframe[
            (dataframe["Date received"] >= time_values[0])
            & (
                dataframe["Date received"]
                <= time_values[1])
        ]
    companyCounts = dataframe["Company"].value_counts()
    companyCounts_sample = companyCounts[:sample_size]
    values_sample = companyCounts_sample.keys().tolist()
    counts_sample = companyCounts_sample.tolist()

    return values_sample, counts_sample


def calculate_dates(dataframe):
    date_data = dataframe["Date received"]
    date_data = date_data
    max_date = (
        date_data.max()
    )  # who doesn't like a good magic number to grab the year from a string?
    min_date = date_data.min()  # - " -
    print('calculate dates -----------------------',min_date, max_date)
    return max_date, min_date


def calculate_n(inp):
    return int(100 / inp)


def make_marks(mini, maxi):
    mini = int(mini)
    maxi = int(maxi)
    ret = {}
    i = 0
    while mini + i <= maxi:
        ret[mini + i] = str(mini + i)
        i += 1
    return ret


def make_options(values):
    ret = []
    for value in values:
        ret.append({"label": value, "value": value})
    return ret


def make_n_marks():
    # TODO: Johan. there must be another way, but for now this will do.
    ret = {}
    i = 0
    while i <= 100:
        if i % 10 == 0:
            ret[i] = str(i) + "%"
        i += 1
    return ret


def add_stopwords(selected_bank):
    STOPWORDS.add("XXXX")
    STOPWORDS.add("XX")
    STOPWORDS.add("xx")
    STOPWORDS.add("xxxx")
    selected_bank_words = re.findall(r"[\w']+", selected_bank)
    for word in selected_bank_words:
        # STOPWORDS.add(word)
        STOPWORDS.add(word.lower())

    print("ADD STOPWORDS")
    print(selected_bank_words)
    return STOPWORDS


def populate_lda_scatter(tsne_lda, lda_model, topic_num, df_dominant_topic):
    topic_top3words = [
        (i, topic)
        for i, topics in lda_model.show_topics(formatted=False)
        for j, (topic, wt) in enumerate(topics)
        if j < 3
    ]

    df_top3words_stacked = pd.DataFrame(topic_top3words, columns=["topic_id", "words"])
    df_top3words = df_top3words_stacked.groupby("topic_id").agg(", \n".join)
    df_top3words.reset_index(level=0, inplace=True)

    tsne_df = pd.DataFrame(
        {
            "tsne_x": tsne_lda[:, 0],
            "tsne_y": tsne_lda[:, 1],
            "topic_num": topic_num,
            "doc_num": df_dominant_topic["Document_No"],
        }
    )
    mycolors = np.array([color for name, color in mcolors.TABLEAU_COLORS.items()])

    # Plot and embed in ipython notebook!
    # for each topic create separate trace
    traces = []
    for topic_id in df_top3words["topic_id"]:
        # print('Topic: {} \nWords: {}'.format(idx, topic))
        tsne_df_f = tsne_df[tsne_df.topic_num == topic_id]
        cluster_name = ", ".join(
            df_top3words[df_top3words["topic_id"] == topic_id]["words"].to_list()
        )
        trace = go.Scatter(
            name=cluster_name,
            x=tsne_df_f["tsne_x"],
            y=tsne_df_f["tsne_y"],
            mode="markers",
            hovertext=tsne_df_f["doc_num"],
            marker=dict(
                size=6,
                color=mycolors[tsne_df_f["topic_num"]],  # set color equal to a variable
                colorscale="Viridis",
                showscale=False,
            ),
        )
        traces.append(trace)

    layout = go.Layout({"title": "Topic analysis using LDA"})

    return {"data": traces, "layout": layout}


def plotly_wordcloud(df):
    complaints_text = list(df["Consumer complaint narrative"].dropna().values)

    ## join all documents in corpus
    text = " ".join(list(complaints_text))

    wc = WordCloud(stopwords=set(STOPWORDS), max_words=100, max_font_size=90)
    wc.generate(text)

    word_list = []
    freq_list = []
    fontsize_list = []
    position_list = []
    orientation_list = []
    color_list = []

    for (word, freq), fontsize, position, orientation, color in wc.layout_:
        word_list.append(word)
        freq_list.append(freq)
        fontsize_list.append(fontsize)
        position_list.append(position)
        orientation_list.append(orientation)
        color_list.append(color)

    # get the positions
    x = []
    y = []
    for i in position_list:
        x.append(i[0])
        y.append(i[1])

    # get the relative occurence frequencies
    new_freq_list = []
    for i in freq_list:
        new_freq_list.append(i * 80)

    trace = go.Scatter(
        x=x,
        y=y,
        textfont=dict(size=new_freq_list, color=color_list),
        hoverinfo="text",
        textposition="top center",
        hovertext=["{0} - {1}".format(w, f) for w, f in zip(word_list, freq_list)],
        mode="text",
        text=word_list,
    )

    layout = go.Layout(
        {
            "xaxis": {
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False,
                "automargin": True,
                "range": [-100, 250],
            },
            "yaxis": {
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False,
                "automargin": True,
                "range": [-100, 450],
            },
            "margin": dict(t=20, b=20, l=10, r=10, pad=4),
        }
    )

    wordcloud_figure_data = {"data": [trace], "layout": layout}

    word_list_top = word_list[:25]
    word_list_top.reverse()
    freq_list_top = freq_list[:25]
    freq_list_top.reverse()

    frequency_figure_data = {
        "data": [
            {
                "y": word_list_top,
                "x": freq_list_top,
                "type": "bar",
                "name": "",
                "orientation": "h",
            }
        ],
        "layout": {"height": "550", "margin": dict(t=20, b=20, l=100, r=20, pad=4)},
    }

    return wordcloud_figure_data, frequency_figure_data


"""
#  Page layout and contents
"""
def Add_Dash(server):
    """Create a Dash app."""
    external_stylesheets = ['/static/dist/css/styles.css',
                            'https://fonts.googleapis.com/css?family=Lato',
                            'https://use.fontawesome.com/releases/v5.8.1/css/all.css']
    external_scripts = ['/static/dist/js/includes/jquery.min.js',
                        '/static/dist/js/main.js']


    # server = flask.flask(__name__)
    # app = dash.Dash(__name__, requests_pathname_prefix='/lda/', external_stylesheets=[dbc.themes.BOOTSTRAP])
    # app.layout = html.Div(children=[navbar, body])

    # def Add_Dash(server):
    #     return dash_app.server
    dash_app = Dash(server=server, #external_stylesheets=[dbc.themes.BOOTSTRAP],
                    external_stylesheets=external_stylesheets,
                    external_scripts=external_scripts,
                    routes_pathname_prefix='/word_cloud/')


    dash_app.index_string = html_layout
    """
    #  Page layout and contents
    """


    global_df = load_data()



    left_column = dbc.Jumbotron(
        [
            html.H4(children="Select host & dataset size", className="display-5"),
            html.Hr(className="my-2"),
            html.Label(
                "Select percentage of dataset (higher is more accurate but also slower)",
                className="lead",
            ),
            dcc.Slider(
                id="n-selection-slider",
                min=1,
                max=100,
                step=1,
                marks=make_n_marks(),
                value=10,
            ),
            # html.Div([
            #     dcc.Markdown(''' --- ''')]),
            html.Label("\n\nSelect a host", style={"marginTop": 100}, className="lead"),
            dcc.Dropdown(id="bank-drop", clearable=False, style={"marginBottom": 50}),
            html.Label("Select Conflict Score", className="lead"),
            html.Div(dcc.RangeSlider(id="time-window-slider",    min=0,
    max=0.3,
    step=None,
    marks={
        0: '0',
        0.01: '1',
        0.05: '2',
        0.1: '3',
        0.2: '4',
        0.3: '5',
    },
    value=[0.1, 0.3]), style={"marginBottom": 50}),
        ]
    )

    lda_plot = dcc.Loading(
        id="loading-lda-plot", children=[dcc.Graph(id="tsne-lda")], type="default"
    )
    lda_table = dcc.Loading(
        id="loading-lda-table",
        children=[
            dash_table.DataTable(
                id="lda-table",
                style_cell_conditional=[
                    {
                        "if": {"column_id": "Text"},
                        "textAlign": "left",
                        "height": "auto",
                        "width": "50%",
                    }
                ],
                style_cell={
                    "padding": "5px",
                    "overflow": "hidden",
                    "textOverflow": "ellipsis",
                    "maxWidth": 0,
                },
                style_header={"backgroundColor": "white", "fontWeight": "bold"},
                style_data={"whiteSpace": "normal", "height": "auto"},
                filter_action="native",
                page_action="native",
                page_current=0,
                page_size=5,
                columns=[],
                data=[],
            )
        ],
        type="default",
    )

    wordcloud_plots = [
        dbc.CardHeader(html.H5("Most popular words in reference titles")),
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Loading(
                                id="loading-wordcloud",
                                children=[dcc.Graph(id="bank-wordcloud")],
                                type="default",
                            ),
                            md=8,
                        ),
                        dbc.Col(
                            dcc.Loading(
                                id="loading-frequencies",
                                children=[dcc.Graph(id="frequency_figure")],
                                type="default",
                            )
                        ),
                    ]
                )
            ]
        ),
    ]

    top_banks_plot = [
        dbc.CardHeader(html.H5("Top 20 domains")),
        dbc.CardBody(
            [
                dcc.Loading(
                    id="loading-banks-hist",
                    children=[dcc.Graph(id="bank-sample")],
                    type="default",
                )
            ]
        ),
    ]

    body = dbc.Container(
        [

            dbc.Row(
                [
                    dbc.Col(left_column, md=5, align="center"),

                ],style={"margin": "auto"},
            ),

            dbc.Card([dbc.Col(wordcloud_plots)],style={"margin": "auto"},),
            # dbc.Row([dbc.Col([lda_plot, lda_table])]),
        ],
        className="mt-12",
    )
    dash_app.layout = html.Div(children=[body])

    """
    #  Callbacks
    """
    @dash_app.callback(
        [
            # Output("time-window-slider", "marks"),
            # Output("time-window-slider", "min"),
            # Output("time-window-slider", "max"),
            # Output("time-window-slider", "step"),
            Output("time-window-slider", "value"),
        ],
        [Input("n-selection-slider", "value")],
    )
    def populate_time_slider(value):
        # print("repopulating time-window-slider")
        max_date, min_date = calculate_dates(global_df)
        print(max_date, min_date)
        print('4/df_tables.ratio.max() --------------------- \n\n\n\n\n',df_tables['Date received'].max())
        print(make_marks(min_date, max_date), int(min_date), max(min_date), 1, [int(min_date), int(max_date)])
        return (

            [int(min_date), int(max_date)],
        )

    @dash_app.callback(Output("bank-drop", "options"), [Input("time-window-slider", "value")])
    def populate_bank_dropdown(time_values):
        print("bank-drop: TODO USE THE TIME VALUES TO LIMIT THE DATASET")
        values, counts = calculate_full(global_df)
        values = global_df.Company.head(100)
        # print("repopulating dropdown")
        return make_options(values)


    @dash_app.callback(
        [Output("bank-wordcloud", "figure"), Output("frequency_figure", "figure")],
        [
            # Input("bank-sample", "clickData"),
            Input("bank-drop", "value"),
            Input("time-window-slider", "value"),
            Input("n-selection-slider", "value"),
        ],
    )
    def update_wordcloud(value_drop, time_values, n_selection):
        if value_drop:
            selected_bank = value_drop
        # elif value_click:
        #     selected_bank = value_click["points"][0]["x"]
        else:
            return {}, {}
        print("redrawing bank-wordcloud...")
        n = float(n_selection / 100)
        print('n_selection ------------------------\n',n_selection)
        print('n\n', n)
        print("got time window:", str(time_values))
        print("got n_selection:", str(n_selection), str(n))

        # sample the dataset according to the slider

        df_tables = load_data_all(selected_bank)
        local_df = sample_data(df_tables, n)
        if time_values is not None:
            # local_df["Date received"] = local_df["Date received"]
            local_df = local_df[
                (local_df["Date received"] >= time_values[0])
                & (
                        local_df["Date received"]
                        <= time_values[1])

                ]
        local_df = local_df[local_df["Company"] == selected_bank]

        add_stopwords(selected_bank)
        wordcloud, frequency_figure = plotly_wordcloud(local_df)

        print("redrawing bank-wordcloud...done")
        return (wordcloud, frequency_figure)


    return dash_app.server



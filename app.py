
# visit http://127.0.0.1:8050/ in your web browser.

from os import environ

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
from flask import Flask
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

from plotting import basic_time_hist
from add_movies import subset_data_table

with open("movies.json",'r') as file:
    movie_json = json.load(file)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

server = Flask(__name__)
app = dash.Dash(
    server=server,
    url_base_pathname=environ.get("JUPYTERHUB_SERVICE_PREFIX", "/"),
    external_stylesheets=external_stylesheets,
)
app.config.suppress_callback_exceptions=True

app.layout = html.Div([
    html.H1('Movie Tracking'),
    dcc.Tabs(id="tabs", value='add_movies', children=[
        dcc.Tab(label='Add/Remove Movies', value='add_movies'),
        dcc.Tab(label='Movie List', value='movie_list'),
        dcc.Tab(label='Plotting', value='plotting'),
    ]),
    html.Div(id='tabs_content'),
    dcc.Store(id="movie_list", data=movie_json),
])

@app.callback(
    Output(component_id='tabs_content', component_property='children'),
    Input(component_id='tabs', component_property='value'),
)
def render_content(tabs):
    if tabs == 'add_movies':
        return add_movies_layout
    elif tabs == 'movie_list':
        return movie_list_layout
    elif tabs == 'plotting':
        return plotting_layout


add_movies_layout = html.Div(
    [
        dcc.Input(id="movie_title"),
        dash_table.DataTable(id="data_table"),
        html.Button('Add movie', id='add_movie'),
        html.Button('Remove movie', id='remove_movie'),  
    ],
)

movie_list_layout = html.Div(
    [
        dash_table.DataTable(id="movie_list_table"),
    ]
)

plotting_layout = html.Div(
    [
        dcc.Dropdown(
            id="graph_type",
            options=[
                {'label': 'Movies vs. Time', 'value': 'num_movies'},
                {'label': 'Genre', 'value': 'genre'},
            ],
            value='num_movies'
        ),
        dcc.Graph(id="graph"),
    ]
)


@app.callback(
    Output(component_id='movie_list', component_property='data'),
    Input(component_id='data_table', component_property='data'),
    Input(component_id='add_movie', component_property='n_clicks'),
    Input(component_id='remove_movie', component_property='n_clicks'),
)
def update_movie_list(data_table, add_movie, remove_movie):
    return None

@app.callback(
    Output(component_id='data_table', component_property='data'),
    Input(component_id='movie_title', component_property='value'),
)
def update_data_table(movie_title):
    return subset_data_table(movie_title)

@app.callback(
    Output(component_id='movie_list_table', component_property='data'),
    Input(component_id='movie_list', component_property='data'),
)
def update_movie_list_output(movie_title):
    with open("movies.json",'r') as file:
        movie_json = json.load(file)
    return movie_json["movies"]

@app.callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='graph_type', component_property='value'),
)
def update_graph(graph_type):
    fig = None
    if graph_type == "num_movies":
        fig = basic_time_hist("monthly")
    elif graph_type == "genre":
        fig = go.Figure()

    return fig


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)

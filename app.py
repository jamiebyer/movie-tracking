
# visit http://127.0.0.1:8050/ in your web browser.

from os import environ

import dash
from dash import dcc, html, dash_table, no_update
from dash.dependencies import Input, Output
from flask import Flask
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

from plotting import basic_time_hist
from add_movies import subset_data_table, add_movie
from layout import tabs_layout, add_movies_layout, movie_list_layout, plotting_layout

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

server = Flask(__name__)
app = dash.Dash(
    server=server,
    url_base_pathname=environ.get("JUPYTERHUB_SERVICE_PREFIX", "/"),
    external_stylesheets=external_stylesheets,
)
app.config.suppress_callback_exceptions=True

app.layout = tabs_layout

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

@app.callback(
    Output(component_id='movie_list', component_property='data'),
    Input(component_id='data_table', component_property='data'),
    Input(component_id='data_table', component_property='selected_rows'),
    Input(component_id='date', component_property='date'),
    Input(component_id='add_movie', component_property='n_clicks'),
    Input(component_id='remove_movie', component_property='n_clicks'),
)
def update_movie_list(data, selected_rows, date, add_movie_button, remove_movie_button):
    if selected_rows is not None and date is not None:
        row = data[selected_rows[0]]
        return add_movie(row, date)
    else:
        return no_update

@app.callback(
    Output(component_id='data_table', component_property='data'),
    Output(component_id='title_type', component_property='options'),
    Output(component_id='genre', component_property='options'),
    Input(component_id='title_type', component_property='value'),
    Input(component_id='primary_title', component_property='value'),
    Input(component_id='start_year', component_property='value'),
    Input(component_id='genre', component_property='value'),
    Input(component_id='exact_match', component_property='value'),
)
def update_data_table(title_type, primary_title, start_year, genre, exact_match):
    return subset_data_table(title_type, primary_title, start_year, genre, exact_match)

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

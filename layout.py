import json
from datetime import date

import dash
from dash import dash_table, dcc, html
from dash.dependencies import Input, Output

with open("movies.json", "r") as file:
    movie_json = json.load(file)

tabs_layout = html.Div(
    [
        html.H1("Movie Tracking"),
        dcc.Tabs(
            id="tabs",
            value="plotting",
            children=[
                dcc.Tab(label="Add/Remove Movies", value="add_movies"),
                dcc.Tab(label="Movie List", value="movie_list"),
                dcc.Tab(label="Plotting", value="plotting"),
            ],
        ),
        html.Div(id="tabs_content"),
        dcc.Store(id="movie_list", data=movie_json),
    ]
)

add_movies_layout = html.Div(
    [
        html.Div(
            [
                dcc.Markdown("Title type"),
                dcc.Dropdown(id="title_type"),
            ]
        ),
        html.Div(
            [
                dcc.Markdown("Primary title"),
                dcc.Input(id="primary_title"),
            ]
        ),
        html.Div(
            [
                dcc.Markdown("Exact match"),
                dcc.Checklist(id="exact_match", options=["Exact match"]),
            ]
        ),
        html.Div(
            [
                dcc.Markdown("Start year"),
                dcc.Input(id="start_year", type="number", step=1),
            ]
        ),
        html.Div(
            [
                dcc.Markdown("Genre"),
                dcc.Dropdown(id="genre"),
            ]
        ),
        dcc.DatePickerSingle(
            id="date",
            month_format="DD-MM-YYYY",
            placeholder="DD-MM-YYYY",
        ),
        html.Button("Add movie", id="add_movie"),
        html.Button("Remove movie", id="remove_movie"),
        dash_table.DataTable(id="data_table", row_selectable="single"),
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
                {"label": "Movies vs. Time", "value": "num_movies"},
                {"label": "Genre", "value": "genre"},
                {"label": "Movie Length", "value": "length"},
                {"label": "Movie Year", "value": "year"},
            ],
            value="num_movies",
        ),
        dcc.Graph(id="graph"),
    ]
)

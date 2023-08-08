import json
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def basic_time_hist(interval):
    with open("movies.json", "r+") as file:
        movie_json = json.load(file)
        dates = []
        for i in movie_json["movies"]:
            dates.append(datetime.strptime(i["date"], "%Y-%m-%d"))
        values, counts = np.unique(dates, return_counts=True)
        df = pd.DataFrame(dict(counts=counts), pd.DatetimeIndex(values, name="dates"))

        if interval == "daily":
            fig = px.bar(df)
        elif interval == "monthly":
            df = df.resample("M").sum()
            df = df.reset_index()
            df["dates"] = df["dates"].apply(lambda x: x.strftime("%Y-%m"))
            df.set_index("dates", inplace=True)
            fig = px.bar(df)
        elif interval == "yearly":
            df = df.resample("Y").sum()
            df = df.reset_index()
            df["dates"] = df["dates"].apply(lambda x: x.strftime("%Y"))
            df.set_index("dates", inplace=True)
            fig = px.bar(df)

        #px.title("movies watched " + interval)

    return fig

def genre_bar():
    with open("movies.json", "r+") as file:
        movie_json = json.load(file)
        genres = []
        for i in movie_json["movies"]:
            genres += i["genres"].split(",")
        values, counts = np.unique(genres, return_counts=True)
        fig = go.Figure(
            data=[
                go.Bar(
                    x=values,
                    y=counts
                )
            ]
        )
    
    return fig

def year_hist():
    with open("movies.json", "r+") as file:
        movie_json = json.load(file)
        years = []
        for i in movie_json["movies"]:
            year = i["startYear"]
            if year.isnumeric():
                years.append(int(year))
        fig = go.Figure(
            data=[
                go.Histogram(
                    x=years,
                    #nbinsx=10,
                )
            ]
        )
    
    return fig

def length_hist():
    with open("movies.json", "r+") as file:
        movie_json = json.load(file)
        lengths = []
        for i in movie_json["movies"]:
            length = i["runtimeMinutes"]
            if length.isnumeric():
                lengths.append(int(length))
        fig = go.Figure(
            data=[
                go.Histogram(
                    x=lengths,
                    #nbinsx=10,
                )
            ]
        )
    
    return fig
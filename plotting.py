from datetime import datetime
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def basic_time_hist(interval, save=False):
    with open("movies.json",'r+') as file:
        movie_json = json.load(file)
        dates = []
        for i in movie_json["movies"]:
            dates.append(datetime.strptime(i["date"], "%d-%m-%Y"))
        values, counts = np.unique(dates, return_counts=True)
        df = pd.DataFrame(dict(counts=counts), pd.DatetimeIndex(values, name='dates'))

        if interval == "daily":
            fig = px.bar(df)
        elif interval == "monthly":
            df = df.resample('M').sum()
            df = df.reset_index()
            df["dates"] = df["dates"].apply(lambda x: x.strftime('%Y-%m'))
            df.set_index('dates', inplace=True)
            fig = px.bar(df)
        elif interval == "yearly":
            df = df.resample('Y').sum()
            df = df.reset_index()
            df["dates"] = df["dates"].apply(lambda x: x.strftime('%Y'))
            df.set_index('dates', inplace=True)
            fig = px.bar(df)

        #px.title("movies watched " + interval)
        
        return fig


from datetime import datetime
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def basic_time_hist(interval, save=False):
    with open("movies.json",'r+') as file:
        movie_json = json.load(file)
        dates = []
        for i in movie_json["movies"]:
            dates.append(datetime.strptime(i["date"], "%d-%m-%Y"))
        values, counts = np.unique(dates, return_counts=True)
        df = pd.DataFrame(dict(counts=counts), pd.DatetimeIndex(values, name='dates'))

        if interval == "daily":
            plt.bar(df.index, df["counts"])
        elif interval == "monthly":
            df = df.resample('M').sum()
            df = df.reset_index()
            df["dates"] = df["dates"].apply(lambda x: x.strftime('%Y-%m'))
            df.set_index('dates', inplace=True)
            plt.bar(df.index, df["counts"])
        elif interval == "yearly":
            df = df.resample('Y').sum()
            df = df.reset_index()
            df["dates"] = df["dates"].apply(lambda x: x.strftime('%Y'))
            df.set_index('dates', inplace=True)
            plt.bar(df.index, df["counts"])

        plt.title("movies watched " + interval)
        plt.tight_layout
        
        if save:
            plt.savefig("figures/basic-time-hist-" + interval + ".png")
        plt.show()


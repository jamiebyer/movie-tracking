import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json

def add_movies(names, dates):
    movie_list = []
    for i in range(len(names)):
        movie_dict = {
            "name": names[i],
            "date": dates[i]
        }
        movie_list.append(movie_dict)

    with open("movies.json",'r+') as file:
        movie_json = json.load(file)
        for movie in movie_list:
            movie_json["movies"].append(movie)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(movie_json, file, indent = 4)
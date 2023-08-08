import json

import dask.dataframe as dd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""
basics_df = dd.read_csv(
    "data/title.basics.tsv/data.tsv", 
    sep='\t', 
    dtype={
        'runtimeMinutes': 'object',
        'startYear': 'object',
        'isAdult': 'object'
        },
        blocksize=25e6
    )
"""
#basics_df = pd.read_csv("data/title.basics.tsv/data.tsv", sep="\t", chunksize=100)

#basics_df = pd.read_csv("data/title.basics.tsv/data.tsv", sep="\t")
#basics_df = basics_df[basics_df["titleType"].isin(["movie", "short"])]
#basics_df = basics_df.drop(["originalTitle", "isAdult", "endYear"], axis=1)
basics_df = {}

# basics_cols = ["startYear", "runtimeMinutes", "genres", "tconst"]

# principals_df = pd.read_csv("data/title.principals.tsv/data.tsv", sep='\t')
# principals_cols = ["nconst"]

# ratings_df = pd.read_csv("data/title.ratings.tsv/data.tsv", sep='\t')
# ratings_cols = ["averageRating"]

# names_df = pd.read_csv("data/name.basics.tsv/data.tsv", sep='\t')
# names_cols = ["primaryName"]


def add_movie(row, date):
    movie_dict = row
    movie_dict["date"] = date

    with open("movies.json", "r+") as file:
        movie_json = json.load(file)
        movie_json["movies"].append(movie_dict)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(movie_json, file, indent=4)
    return movie_json


def subset_data_table(title_type, primary_title, start_year, genre, exact_match):
    df = basics_df
    if title_type is not None:
        df = df.loc[df["titleType"] == title_type]
        #df = df.query("titleType == '" + title_type + "'")
    if primary_title is not None:
        if exact_match:
            df = df.loc[df["primaryTitle"].str.lower() == primary_title]
            #df = df.query("primaryTitle.str.lower() == '" + primary_title + "'")
        else:
            df = df.loc[
                df["primaryTitle"].str.lower().str.contains(primary_title, na=False)
            ]
            #df = df.query(
            #    "primaryTitle.str.lower().str.contains('" + primary_title + "', na=False)"
            #)
    if start_year is not None:
        df = df.loc[df["startYear"] == start_year]
        #df = df.query["startYear == " + str(start_year)]
    #if genre is not None:
    #    df = df[[genre in g for g in df["genres"]]]

    #print(df.shape)
    #data = df.head(5, npartitions=-1)
    data = df.head(30)

    title_type_options = np.unique(data["titleType"])

    genre_options = []
    for g in data["genres"].values:
        genre_options += g.split(",")
    genre_options = np.unique(genre_options)
    return data.to_dict("records"), title_type_options, genre_options

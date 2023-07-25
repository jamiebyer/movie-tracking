import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json

basics_df = pd.read_csv("data/title.basics.tsv/data.tsv", sep='\t')
basics_df = basics_df[basics_df["titleType"].isin(["movie", "short"])]
basics_cols = ["startYear", "runtimeMinutes", "genres", "tconst"]

#principals_df = pd.read_csv("data/title.principals.tsv/data.tsv", sep='\t')
#principals_cols = ["nconst"]

#ratings_df = pd.read_csv("data/title.ratings.tsv/data.tsv", sep='\t')
#ratings_cols = ["averageRating"]

#names_df = pd.read_csv("data/name.basics.tsv/data.tsv", sep='\t')
#names_cols = ["primaryName"]

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


# data from: https://www.imdb.com/interfaces/
def add_ind_imdb_info(movie_dict, df, cols, name_type):
    if name_type == "primaryTitle":
        name = movie_dict["name"]
        movie_info = df.loc[df["primaryTitle"].str.lower() == name]
    elif name_type == "tconst":
        name = movie_dict["tconst"]
        movie_info = df.loc[df["tconst"] == name]
    elif name_type == "nconst":
        name = movie_dict["nconst"]
        movie_info = df.loc[df["nconst"] == name]
    
    if len(movie_info) != 1:
        try:
            movie_info = movie_info[movie_info["startYear"] == movie_dict["startYear"]]
            if movie_dict["startYear"] == "NA":
                for col in cols:
                    movie_dict[col] = "NA"
            if len(movie_info) == 1:
                for col in cols:
                    movie_info.reset_index()
                    movie_dict[col] = movie_info[col].iloc[0]    
            else:
                print(name)
                print(movie_info)
        except:
            print(name)
            pd.options.display.max_columns = None
            print(movie_info)
    else:
        for col in cols:
            movie_info.reset_index()
            movie_dict[col] = movie_info[col].iloc[0]    
    

    
    return movie_dict

def add_all_imdb_info():
    basics_df = pd.read_csv("data/title.basics.tsv/data.tsv", sep='\t')
    basics_df = basics_df[basics_df["titleType"].isin(["movie", "short"])]
    basics_cols = ["startYear", "runtimeMinutes", "genres", "tconst"]

    #principals_df = pd.read_csv("data/title.principals.tsv/data.tsv", sep='\t')
    #principals_cols = ["nconst"]

    #ratings_df = pd.read_csv("data/title.ratings.tsv/data.tsv", sep='\t')
    #ratings_cols = ["averageRating"]

    #names_df = pd.read_csv("data/name.basics.tsv/data.tsv", sep='\t')
    #names_cols = ["primaryName"]

    print("starting loop")
    with open("movies.json",'r+') as file:
        movie_json = json.load(file)
        for i in range(len(movie_json["movies"])):
            movie_dict = movie_json["movies"][i]
            movie_dict = add_ind_imdb_info(movie_dict, basics_df, basics_cols, "primaryTitle")
            #movie_dict = add_ind_imdb_info(movie_dict, principals_df, principals_cols, "tconst")
            #movie_dict = add_ind_imdb_info(movie_dict, ratings_df, ratings_cols, "tconst")            
            movie_json["movies"][i] = movie_dict
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(movie_json, file, indent = 4)


def subset_data_table(movie_title):
    if movie_title is not None:
        movie_info = basics_df.loc[basics_df["primaryTitle"].str.lower() == movie_title]#.head(10)
        data = movie_info.to_dict('records')
        return data
    else:
        return None



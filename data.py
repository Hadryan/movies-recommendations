import json
import pandas as pd
import numpy as np


def create_df():
    t1 = pd.read_csv('data/user_ratedmovies.dat', sep='\t', nrows=10000)
    t2 = pd.read_csv('data/movie_genres.dat', sep='\t').groupby(
        ['movieID']).agg(lambda col: '|'.join('genre-' + col))
    t2 = t2.join(t2.pop('genre').str.get_dummies('|'))
    return pd.merge(t1, t2, on='movieID')


def df_to_json(df):
    json_df = []
    genre_keys = set()
    for _, row in df.iterrows():
        row_json = row.to_dict()
        row_json['userID'] = str(int(row_json['userID']))
        row_json['movieID'] = str(int(row_json['movieID']))
        for k in row_json:
            if k.startswith('genre-'):
                genre_keys.add(k)
        json_df.append(row_json)
    return json_df, genre_keys


def df_to_dict(df):
    json_df = []
    for _, row in df.iterrows():
        row_json = row.to_dict()
        row_json['userID'] = int(row_json['userID'])
        row_json['movieID'] = int(row_json['movieID'])
        json_df.append(row_json)
    return json_df


def dict_list_to_df(dl):
    return pd.DataFrame(dl)


def dict_list_mean(dl, keys):
    g = {}
    for i in keys:
        l = []
        for d in dl:
            if d[i] == 1:
                l.append(d['rating'])
        if l:
             g[i] = np.nanmean(l)
        else:
            g[i] = 0
    return g


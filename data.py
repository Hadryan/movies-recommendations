import json
import pandas as pd
import numpy as np


def create_df():
    t1 = pd.read_csv('data/user_ratedmovies.dat', sep='\t', nrows=1000)
    t2 = pd.read_csv('data/movie_genres.dat', sep='\t').groupby(
        ['movieID']).agg(lambda col: '|'.join('genre_' + col))
    t2 = t2.join(t2.pop('genre').str.get_dummies('|'))
    return pd.merge(t1, t2, on='movieID')


def df_to_json(df):
    json_df = []
    genre_keys = set()
    for _, row in df.iterrows():
        row_json = row.to_dict()
        row_json['movie_id'] = str(int(row_json.pop('movieID')))
        row_json['user_id'] = str(int(row_json.pop('userID')))
        row_json = {k.lower(): v for k, v in row_json.items()}
        for k in row_json:
            if k not in ('movie_id', 'user_id'):
                row_json[k] = int(row_json[k])
            if '-' in k:
                new_key = k.replace('-', '_')
                row_json[new_key] = row_json.pop(k)
                if k.startswith('genre_'):
                    genre_keys.add(new_key)

        json_df.append(row_json)
    return json_df, genre_keys


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

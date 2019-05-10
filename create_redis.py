import db
from data import df_to_json, create_df, dict_list_mean

DB, DB_GENRE_KEYS = df_to_json(create_df())

for i in DB:
    db.create('all', i)

for i in DB_GENRE_KEYS:
    db.create('keys', i)


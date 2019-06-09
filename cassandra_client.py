def create_keyspace(session, keyspace):
    session.execute(f"""
CREATE KEYSPACE IF NOT EXISTS {keyspace}
WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': '1' }}
""")


def create_table(session, keyspace, table):
    session.execute(f"""
CREATE TABLE IF NOT EXISTS {keyspace}.{table} (
user_id text, movie_id text, rating int,
date_day int, date_month int, date_year int, date_hour int, date_minute int, date_second int,
genre_action int,
genre_adventure int,
genre_animation int,
genre_children int,
genre_comedy int,
genre_crime int,
genre_documentary int,
genre_drama int,
genre_fantasy int,
genre_film_noir int,
genre_horror int,
genre_imax int,
genre_musical int,
genre_mystery int,
genre_romance int,
genre_sci_fi int,
genre_short int,
genre_thriller int,
genre_war int,
genre_western int,

PRIMARY KEY(user_id)
)
""")


def push_table(session, keyspace, table, rating):
    session.execute(f"""
INSERT INTO {keyspace}.{table} (user_id, movie_id, rating,
date_day, date_month, date_year, date_hour, date_minute, date_second,
genre_action, genre_adventure, genre_animation, genre_children, genre_comedy, genre_crime, genre_documentary,
genre_drama, genre_fantasy, genre_film_noir, genre_horror, genre_imax, genre_musical, genre_mystery, genre_romance,
genre_sci_fi, genre_short, genre_thriller, genre_war, genre_western
)
VALUES (
%(user_id)s, %(movie_id)s, %(rating)s,
%(date_day)s, %(date_month)s, %(date_year)s, %(date_hour)s, %(date_minute)s, %(date_second)s,
%(genre_action)s , %(genre_adventure)s , %(genre_animation)s, %(genre_children)s, %(genre_comedy)s, %(genre_crime)s,
%(genre_documentary)s, %(genre_drama)s, %(genre_fantasy)s, %(genre_film_noir)s, %(genre_horror)s, %(genre_imax)s,
%(genre_musical)s, %(genre_mystery)s, %(genre_romance)s, %(genre_sci_fi)s, %(genre_short)s, %(genre_thriller)s,
 %(genre_war)s, %(genre_western)s
)
""", rating
                    )


def list_table(session, keyspace, table):
    rows = session.execute(f"SELECT * FROM {keyspace}.{table};")
    if rows is None:
        return []
    return list(rows)


def clear_table(session, keyspace, table):
    session.execute(f"TRUNCATE {keyspace}.{table};")

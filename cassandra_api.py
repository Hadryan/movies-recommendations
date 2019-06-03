from cassandra.query import dict_factory
from cassandra.cluster import Cluster
import cassandra_client as client


KEYSPACE = "user_ratings"
TABLE = "ratings"
SESSION = Cluster(['127.0.0.1'], port=9042).connect()

client.create_keyspace(SESSION, KEYSPACE)
client.create_table(SESSION, KEYSPACE, TABLE)

SESSION.set_keyspace(KEYSPACE)
SESSION.row_factory = dict_factory
RATING_QUERY = SESSION.prepare(f"SELECT * FROM {TABLE} WHERE user_id=?")
DELETE_RATING_QUERY = SESSION.prepare(f"DELETE FROM {TABLE} WHERE user_id=?")


def get(user_id: str) -> dict:
    user = SESSION.execute(RATING_QUERY, [user_id])
    if user:
        return user[0]
    return {}


def push(rating: dict):
    client.push_table(SESSION, KEYSPACE, TABLE, rating)


def list() -> list:
    return client.list_table(SESSION, KEYSPACE, TABLE)


def delete(user_id: str):
    SESSION.execute(DELETE_RATING_QUERY, [user_id])


def clear():
    client.clear_table(SESSION, KEYSPACE, TABLE)

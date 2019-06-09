import pandas as pd
from elasticsearch import Elasticsearch, helpers
import numpy as np


class ElasticClient:
    def __init__(self, address='localhost:10000'):
        self.es = Elasticsearch(address)

    def index_documents(self):
        df = pd.read_csv('data/user_ratedmovies.dat', delimiter='\t').loc[:, ['userID', 'movieID', 'rating']]
        means = df.groupby(['userID'], as_index=False, sort=False).mean().loc[:, [
            'userID', 'rating']].rename(columns={'rating': 'ratingMean'})
        df = pd.merge(df, means, on='userID', how="left", sort=False)
        df['ratingNormal'] = df['rating'] - df['ratingMean']
        ratings = df.loc[:, ['userID', 'movieID', 'ratingNormal']].rename(
            columns={'ratingNormal': 'rating'}).pivot_table(
                index='userID', columns='movieID', values='rating').fillna(0)
        print("Indexing users...")
        index_users = [{
            "_index": "users",
            "_type": "user",
            "_id": index,
            "_source": {
                'ratings': row[row > 0]
                .sort_values(ascending=False)
                .index.values.tolist()
            }
        } for index, row in ratings.iterrows()]
        helpers.bulk(self.es, index_users)
        print("Done")
        print("Indexing movies...")
        index_movies = [{
            "_index": "movies",
            "_type": "movie",
            "_id": column,
            "_source": {
                "whoRated": ratings[column][ratings[column] > 0]
                .sort_values(ascending=False)
                .index.values.tolist()
            }
        } for column in ratings]
        helpers.bulk(self.es, index_movies)
        print("Done")

    def get_movies_liked_by_user(self, user_id, index='users'):
        user_id = int(user_id)
        return self.es.get(index=index, doc_type="user", id=user_id)["_source"]

    def get_users_that_like_movie(self, movie_id, index='movies'):
        movie_id = int(movie_id)
        return self.es.get(index=index, doc_type="movie", id=movie_id)["_source"]

    def get_doc(self, _id, index, doc_type):
        return self.es.get(index=index, doc_type=doc_type, id=int(_id))

    def get_movies_doc(self, _id):
        return self.get_doc(_id, 'movies', 'movie')

    def get_users_doc(self, _id):
        return self.get_doc(_id, 'users', 'user')

    def add_doc(self, _id, doc, index, doc_type):
        self.es.create(index=index, id=int(_id), body=doc, doc_type=doc_type)

    def add_movies_doc(self, _id, who_rated):
        self.add_doc(_id, {'whoRated': who_rated}, 'movies', 'movie')

    def add_users_doc(self, _id, ratings):
        self.add_doc(_id, {'ratings': ratings}, 'users', 'user')
        self._update_ratings(_id, ratings)

    def update_doc(self, _id, doc, index, doc_type):
        self.es.update(index=index, id=int(_id), doc_type=doc_type, body={'doc': doc})

    def update_movies_doc(self, _id, who_rated):
        self.update_doc(_id, {'whoRated': who_rated}, 'movies', 'movie')

    def update_users_doc(self, _id, ratings):
        self._update_ratings(_id, ratings)
        self.update_doc(_id, {'ratings': ratings}, 'users', 'user')

    def _update_ratings(self, _id, ratings):
        _id = int(_id)
        old_ratings = list(set(self.get_movies_liked_by_user(_id)['ratings']) - set(ratings))
        for movie in ratings:
            who_rated = self.get_movies_doc(movie)['_source']['whoRated']
            if _id not in who_rated:
                who_rated.append(_id)
                self.update_movies_doc(movie, who_rated)

        for movie in old_ratings:
            who_rated = self.get_movies_doc(movie)['_source']['whoRated']
            who_rated.remove(_id)
            self.update_movies_doc(movie, who_rated)

    def rm_doc(self, _id, index, doc_type):
        self.es.delete(index, int(_id), doc_type=doc_type)

    def rm_movies_doc(self, _id):
        self.rm_doc(_id, 'movies', 'movie')

    def rm_users_doc(self, _id):
        _id = int(_id)
        user_movies = self.get_movies_liked_by_user(_id)['ratings']
        for movie in user_movies:
            who_rated = self.get_movies_doc(movie)['_source']['whoRated']
            who_rated.remove(_id)
            self.update_movies_doc(movie, who_rated)
        self.rm_doc(_id, 'users', 'user')

    def preselect_movies(self, user_id):
        user_movies = self.get_movies_liked_by_user(user_id)['ratings']
        res = self.es.search(
            index='users',
            body={
                'query': {
                    'bool': {
                        'must': {
                            'terms': {
                                'ratings': user_movies
                            }
                        },
                    }
                }
            },
            size=10,
        )['hits']['hits']

        return list({j for i in res for j in i['_source']['ratings']} - set(user_movies))[:10]

    def preselect_users(self, movie_id):
        movie_users = self.get_users_that_like_movie(movie_id)['whoRated']
        res = self.es.search(
            index='movies',
            body={
                'query': {
                    'bool': {
                        'must': {
                            'terms': {
                                'whoRated': movie_users
                            }
                        },
                    }
                }
            },
            size=10,
        )['hits']['hits']

        return list({j for i in res for j in i['_source']['whoRated']} - set(movie_users))[:10]

    def list_index(self, index):
        return self.es.search(
            index=index,
            body={'query': {
                'match_all': {}}
            }
        )

    def stats(self, index):
        return self.es.indices.stats(index=index)


if __name__ == "__main__":
    ec = ElasticClient()

    # test data for 1000 rows:
    # user: 75
    # movie 296

    ec.index_documents()

    res = ec.preselect_movies(75)
    assert len(res) > 0
    movies_test_user = ec.get_movies_liked_by_user(75)['ratings']
    for movie in res:
        assert movie not in movies_test_user
        _ = ec.get_doc(movie, 'movies', 'movie')  # raises exception if movie is not found in elastic search

    res = ec.preselect_users(296)
    assert len(res) > 0
    users_test_movie = ec.get_users_that_like_movie(296)['whoRated']
    for user in res:
        assert user not in users_test_movie
        _ = ec.get_doc(user, 'users', 'user')  # raises exception if user is not found in elastic search

import json
from flask import Flask, request, Response
from cheroot.wsgi import Server, PathInfoDispatcher
import random

from data import dict_list_mean
import cassandra_api as cassy
import elasticsearch_client

app = Flask(__name__)

QUEUE_ALL, QUEUE_KEYS = 'all', 'keys'

KEYS = {'genre_action', 'genre_adventure', 'genre_animation', 'genre_children', 'genre_comedy', 'genre_crime',
        'genre_documentary', 'genre_drama', 'genre_fantasy', 'genre_film_noir', 'genre_horror', 'genre_imax',
        'genre_musical', 'genre_mystery', 'genre_romance', 'genre_sci_fi', 'genre_short', 'genre_thriller',
        'genre_war', 'genre_western', 'movie_id', 'user_id'}


ec = elasticsearch_client.ElasticClient()


def json_res(obj: dict, code: int):
    return Response(json.dumps(obj), code, mimetype='application/json')


@app.route('/ratings', methods=['GET', 'POST', 'DELETE'])
def ratings_route():
    if request.method == 'POST':
        cassy.push(request.get_json(force=True))
        return json_res({}, 201)
    elif request.method == 'DELETE':
        cassy.clear()
        return json_res({}, 204)

    return json_res(cassy.list(), 200)


@app.route('/ratings/users/<user_id>', methods=['GET', 'DELETE'])
def users_rating_route(user_id):
    if request.method == 'DELETE':
        cassy.delete(user_id)
        return json_res({}, 204)
        # return json_res({'error': 'Not found'}, 404)

    return json_res(cassy.get(user_id), 200)
    # return json_res({'error': 'Not found'}, 404)


@app.route('/ratings/genre/avg', methods=['GET'])
def avg_genre_ratings_route():
    g = dict_list_mean(cassy.list(), KEYS)
    return json_res(g, 200)


@app.route('/ratings/genre/avg/<user_id>', methods=['GET'])
def avg_genre_ratings_user_route(user_id):
    db_user = [cassy.get(user_id)]
    g = dict_list_mean(db_user, KEYS)
    return json_res(g, 200)


@app.route('/ratings/genre/avg/random/profile', methods=['GET'])
def avg_genre_ratings_user_random_profile_route():
    _db = cassy.list()
    g = dict_list_mean(_db, KEYS)
    user_id = _db[random.randint(0, len(_db)-1)]['user_id']
    db_user = [x for x in _db if x['user_id'] == user_id]
    g_user = dict_list_mean(db_user, KEYS)
    prof = {}
    for i in KEYS:
        prof[i] = g[i] - g_user[i]
    prof['user_id'] = user_id
    return json_res(prof, 200)


@app.route('/ratings/genre/avg/<user_id>/profile', methods=['GET'])
def avg_genre_ratings_user_profile_route(user_id):
    _db = cassy.list()
    g = dict_list_mean(_db, KEYS)
    db_user = [x for x in _db if x['user_id'] == user_id]
    g_user = dict_list_mean(db_user, KEYS)
    prof = {}
    for i in KEYS:
        prof[i] = g[i] - g_user[i]
    return json_res(prof, 200)


@app.route('/documents/users/<int:user_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_doc(user_id):
    if request.method == 'POST':
        try:
            _ = ec.get_users_doc(user_id)
            return json_res({'error': 'Item exists'}, 400)
        except:
            pass
        ec.add_users_doc(user_id, request.get_json(force=True))
        return json_res({}, 201)

    if request.method == 'PUT':
        try:
            _ = ec.get_users_doc(user_id)
        except:
            return json_res({'error': 'Not found'}, 404)
        ec.update_users_doc(user_id, request.get_json(force=True))
        return json_res({}, 201)

    if request.method == 'DELETE':
        try:
            ec.rm_users_doc(user_id)
            return json_res({}, 204)
        except:
            return json_res({'error': 'Not found'}, 404)

    try:
        return json_res(ec.get_users_doc(user_id), 200)
    except:
        return json_res({'error': 'Not found'}, 404)


@app.route('/documents/movies/<int:movie_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def movie_doc(movie_id):
    if request.method == 'POST':
        try:
            _ = ec.get_movies_doc(movie_id)
            return json_res({'error': 'Item exists'}, 400)
        except:
            pass
        ec.add_movies_doc(movie_id, request.get_json(force=True))
        return json_res({}, 201)

    if request.method == 'PUT':
        try:
            _ = ec.get_movies_doc(movie_id)
        except:
            return json_res({'error': 'Not found'}, 404)
        ec.update_movies_doc(movie_id, request.get_json(force=True))
        return json_res({}, 201)

    if request.method == 'DELETE':
        try:
            ec.rm_movies_doc(movie_id)
            return json_res({}, 204)
        except:
            return json_res({'error': 'Not found'}, 404)

    try:
        return json_res(ec.get_movies_doc(movie_id), 200)
    except:
        return json_res({'error': 'Not found'}, 404)


@app.route('/documents/users/<int:user_id>/preselection', methods=['GET'])
def user_doc_preselection(user_id):
    try:
        return json_res(ec.preselect_movies(user_id), 200)
    except:
        return json_res({'error': 'Not found'}, 404)


@app.route('/documents/movies/<int:movie_id>/preselection', methods=['GET'])
def movie_doc_preselection(movie_id):
    try:
        return json_res(ec.preselect_users(movie_id), 200)
    except:
        return json_res({'error': 'Not found'}, 404)


if __name__ == '__main__':
    # Flask
    app.run(debug=True)

    # Cheroot
    # server = Server(('localhost', 5000), PathInfoDispatcher({'/': app}))
    # try:
    #     server.start()
    # except KeyboardInterrupt:
    #     server.stop()

import json
from flask import Flask, request, Response
from cheroot.wsgi import Server, PathInfoDispatcher
import random

import db
from data import dict_list_mean

app = Flask(__name__)

QUEUE_ALL, QUEUE_KEYS = 'all', 'keys'


def json_res(obj: dict, code: int):
    return Response(json.dumps(obj), code, mimetype='application/json')


@app.route('/ratings', methods=['GET', 'POST', 'DELETE'])
def ratings_route():
    if request.method == 'POST':
        db.create(QUEUE_ALL, json.dumps(request.get_json(force=True)))
        return json_res({}, 201)
    elif request.method == 'DELETE':
        db.clear()
        return json_res({}, 204)

    return json_res(db.list(QUEUE_ALL), 200)


@app.route('/ratings/users/<user_id>', methods=['GET', 'DELETE'])
def users_rating_route(user_id):
    _db = db.list(QUEUE_ALL)
    if request.method == 'DELETE':
        for ind, i in enumerate(_db):
            if i.get('userID') == user_id:
                db.rm_index(QUEUE_ALL, ind)
                return json_res({}, 204)
        return json_res({'error': 'Not found'}, 404)

    for i in _db:
        if i.get('userID') == user_id:
            return json_res(i, 200)
    return json_res({'error': 'Not found'}, 404)


@app.route('/ratings/movies/<movie_id>', methods=['GET', 'DELETE'])
def movies_rating_route(movie_id):
    _db = db.list(QUEUE_ALL)
    if request.method == 'DELETE':
        for ind, i in enumerate(_db):
            if i.get('movieID') == movie_id:
                db.rm_index(QUEUE_ALL, ind)
                return json_res({}, 204)
        return json_res({'error': 'Not found'}, 404)

    for i in _db:
        if i.get('movieID') == movie_id:
            return json_res(i, 200)
    return json_res({'error': 'Not found'}, 404)


@app.route('/ratings/genre/avg', methods=['GET'])
def avg_genre_ratings_route():
    g = dict_list_mean(db.list(QUEUE_ALL), db.list(QUEUE_KEYS))
    return json_res(g, 200)


@app.route('/ratings/genre/avg/<user_id>', methods=['GET'])
def avg_genre_ratings_user_route(user_id):
    db_user = [x for x in db.list(QUEUE_ALL) if x['userID'] == user_id]
    g = dict_list_mean(db_user, db.list(QUEUE_KEYS))
    return json_res(g, 200)


@app.route('/ratings/genre/avg/random/profile', methods=['GET'])
def avg_genre_ratings_user_random_profile_route():
    _db = db.list(QUEUE_ALL)
    g = dict_list_mean(_db, db.list(QUEUE_KEYS))
    user_id = _db[random.randint(0, len(_db))]['userID']
    db_user = [x for x in _db if x['userID'] == user_id]
    g_user = dict_list_mean(db_user, db.list(QUEUE_KEYS))
    prof = {}
    for i in db.list(QUEUE_KEYS):
        prof[i] = g[i] - g_user[i]
    prof['userID'] = user_id
    return json_res(prof, 200)


@app.route('/ratings/genre/avg/<user_id>/profile', methods=['GET'])
def avg_genre_ratings_user_profile_route(user_id):
    _db = db.list(QUEUE_ALL)
    g = dict_list_mean(_db, db.list(QUEUE_KEYS))
    db_user = [x for x in _db if x['userID'] == user_id]
    g_user = dict_list_mean(db_user, db.list(QUEUE_KEYS))
    prof = {}
    for i in db.list(QUEUE_KEYS):
        prof[i] = g[i] - g_user[i]
    return json_res(prof, 200)


if __name__ == '__main__':
    # Flask
    # app.run(debug=True)

    # Cheroot
    server = Server(('localhost', 5000), PathInfoDispatcher({'/': app}))
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()

import requests
from time import sleep
import sys

_TEST_URL = f'http://localhost:5000/ratings'
sys.stdout = open('client_out.txt', 'w')


def print_req(req):
    print(req.status_code)
    print(req.headers)
    try:
        req_json = req.json()
    except:
        req_json = req.content
    if isinstance(req_json, list) and len(req_json) > 10:
        req_json = req_json[0:10]
    print(req_json, end='\n\n')


print(f'[GET] {_TEST_URL}')
print_req(requests.get(_TEST_URL))
sleep(0.1)

print(f'[DELETE] {_TEST_URL}')
print_req(requests.delete(_TEST_URL))
sleep(0.1)

print(f'[GET] {_TEST_URL}')
print_req(requests.get(_TEST_URL))
sleep(0.1)

print(f'[POST] {_TEST_URL}')
print_req(requests.post(_TEST_URL, json={'rating': 5, 'date_day': 7, 'date_month': 5, 'date_year': 2004,
                                         'date_hour': 23, 'date_minute': 32, 'date_second': 18, 'genre_action': 0,
                                         'genre_adventure': 0, 'genre_animation': 0, 'genre_children': 0,
                                         'genre_comedy': 0, 'genre_crime': 0, 'genre_documentary': 0, 'genre_drama': 0,
                                         'genre_fantasy': 0, 'genre_film_noir': 0, 'genre_horror': 0, 'genre_imax': 0,
                                         'genre_musical': 0, 'genre_mystery': 0, 'genre_romance': 0, 'genre_sci_fi': 1,
                                         'genre_short': 0, 'genre_thriller': 1, 'genre_war': 0, 'genre_western': 0,
                                         'movie_id': 'test', 'user_id': 'test'}))
sleep(0.1)

print(f'[POST] {_TEST_URL}')
print_req(requests.post(_TEST_URL, json={'rating': 3, 'date_day': 7, 'date_month': 5, 'date_year': 2004,
                                         'date_hour': 23, 'date_minute': 32, 'date_second': 18, 'genre_action': 0,
                                         'genre_adventure': 0, 'genre_animation': 0, 'genre_children': 0,
                                         'genre_comedy': 0, 'genre_crime': 1, 'genre_documentary': 0, 'genre_drama': 1,
                                         'genre_fantasy': 0, 'genre_film_noir': 0, 'genre_horror': 0, 'genre_imax': 1,
                                         'genre_musical': 0, 'genre_mystery': 0, 'genre_romance': 0, 'genre_sci_fi': 0,
                                         'genre_short': 0, 'genre_thriller': 1, 'genre_war': 0, 'genre_western': 0,
                                         'movie_id': 'test1', 'user_id': 'test1'}))
sleep(0.1)

print(f'[POST] {_TEST_URL}')
print_req(requests.post(_TEST_URL, json={'rating': 4, 'date_day': 7, 'date_month': 5, 'date_year': 2004,
                                         'date_hour': 23, 'date_minute': 32, 'date_second': 18, 'genre_action': 0,
                                         'genre_adventure': 0, 'genre_animation': 0, 'genre_children': 0,
                                         'genre_comedy': 0, 'genre_crime': 0, 'genre_documentary': 0, 'genre_drama': 0,
                                         'genre_fantasy': 0, 'genre_film_noir': 0, 'genre_horror': 0, 'genre_imax': 0,
                                         'genre_musical': 0, 'genre_mystery': 0, 'genre_romance': 0, 'genre_sci_fi': 1,
                                         'genre_short': 0, 'genre_thriller': 1, 'genre_war': 0, 'genre_western': 0,
                                         'movie_id': 'test', 'user_id': 'test2'}))
sleep(0.1)

url = f'{_TEST_URL}/users/test'
print(f'[GET] {url}')
print_req(requests.get(url))
sleep(0.1)

url = f'{_TEST_URL}/genre/avg'
print(f'[GET] {url}')
print_req(requests.get(url))
sleep(0.1)

url = f'{_TEST_URL}/genre/avg/test'
print(f'[GET] {url}')
print_req(requests.get(url))
sleep(0.1)

url = f'{_TEST_URL}/genre/avg/test/profile'
print(f'[GET] {url}')
print_req(requests.get(url))
sleep(0.1)

url = f'{_TEST_URL}/genre/avg/random/profile'
print(f'[GET] {url}')
print_req(requests.get(url))
sleep(0.1)


url = f'{_TEST_URL}/users/test'
print(f'[DELETE] {url}')
print_req(requests.delete(url))
sleep(0.1)

print(f'[DELETE] {_TEST_URL}')
print_req(requests.delete(_TEST_URL))
sleep(0.1)

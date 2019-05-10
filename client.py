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

print(f'[POST] {_TEST_URL}')
print_req(requests.post(_TEST_URL, json={"userID": "000", "movieID": "3", "rating": 1.0, "date_day": 29.0, "date_month": 10.5, "date_year": 2006.0, "date_hour": 23.0, "date_minute": 17.0, "date_second": 16.0, "genre-Action": 0.5, "genre-Adventure": 0.5, "genre-Animation": 0.5, "genre-Children": 0.5, "genre-Comedy": 1.0,
                                         "genre-Crime": 0.5, "genre-Documentary": 0.5, "genre-Drama": 0.5, "genre-Fantasy": 0.5, "genre-Film-Noir": 0.5, "genre-Horror": 0.5, "genre-IMAX": 0.5, "genre-Musical": 0.5, "genre-Mystery": 0.5, "genre-Romance": 1.0, "genre-Sci-Fi": 0.5, "genre-Short": 0.5, "genre-Thriller": 0.5, "genre-War": 0.5, "genre-Western": 0.5}))
sleep(0.1)

url = f'{_TEST_URL}/users/000'
print(f'[GET] {url}')
print_req(requests.get(url))
sleep(0.1)

print(f'[DELETE] {url}')
print_req(requests.delete(url))
sleep(0.1)

url = f'{_TEST_URL}/movies/32'
print(f'[GET] {url}')
print_req(requests.get(url))
sleep(0.1)

print(f'[DELETE] {url}')
print_req(requests.delete(url))
sleep(0.1)

url = f'{_TEST_URL}/genre/avg'
print(f'[GET] {url}')
print_req(requests.get(url))
sleep(0.1)

url = f'{_TEST_URL}/genre/avg/78'
print(f'[GET] {url}')
print_req(requests.get(url))
sleep(0.1)

url = f'{_TEST_URL}/genre/avg/78/profile'
print(f'[GET] {url}')
print_req(requests.get(url))
sleep(0.1)

url = f'{_TEST_URL}/genre/avg/random/profile'
print(f'[GET] {url}')
print_req(requests.get(url))
sleep(0.1)


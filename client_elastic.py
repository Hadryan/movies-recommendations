import requests
import sys
from time import sleep

_URL = f'http://localhost:5000/documents'
sys.stdout = open('client_out.txt', 'w')


def _print_req(req):
    print(req.status_code)
    print(req.headers)
    try:
        req_json = req.json()
    except:
        req_json = req.content
    print(req_json, end='\n\n')


def _get(url):
    print(f'[GET] {url}')
    _print_req(requests.get(url))


def _post(url, body):
    print(f'[POST] {url}')
    _print_req(requests.post(url, json=body))


def _put(url, body):
    print(f'[PUT] {url}')
    _print_req(requests.put(url, json=body))


def _delete(url):
    print(f'[DELETE] {url}')
    _print_req(requests.delete(url))


_get(f'{_URL}/users/75')
_get(f'{_URL}/users/0')
_get(f'{_URL}/movies/3')
_get(f'{_URL}/movies/0')

_get(f'{_URL}/users/75/preselection')
_get(f'{_URL}/movies/3/preselection')

_post(f'{_URL}/movies/80000', [])
_post(f'{_URL}/movies/80001', [])
_post(f'{_URL}/movies/80002', [])

_get(f'{_URL}/movies/80000')
_get(f'{_URL}/movies/80001')
_get(f'{_URL}/movies/80002')

_post(f'{_URL}/users/90000', [80000, 80001])
_get(f'{_URL}/users/90000')

_get(f'{_URL}/movies/80000')
_get(f'{_URL}/movies/80001')
_get(f'{_URL}/movies/80002')

_put(f'{_URL}/users/90000', [80000, 80002])
_get(f'{_URL}/users/90000')
_get(f'{_URL}/movies/80000')
_get(f'{_URL}/movies/80001')
_get(f'{_URL}/movies/80002')

_post(f'{_URL}/users/90001', [80000])
_get(f'{_URL}/users/90001')
sleep(1)  # wait for elastic
_get(f'{_URL}/users/90001/preselection')

_delete(f'{_URL}/users/90000')
_delete(f'{_URL}/users/90001')
_get(f'{_URL}/movies/80000')
_get(f'{_URL}/movies/80001')
_get(f'{_URL}/movies/80002')

_delete(f'{_URL}/movies/80000')
_delete(f'{_URL}/movies/80001')
_delete(f'{_URL}/movies/80002')

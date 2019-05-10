from redis import StrictRedis
from redis_queue import pull, rm_first, clear_all, publish, pull_all, rm_at
import json

redis_cli = StrictRedis(port=6381)


def get(queue_name):
    res = pull(redis_cli, queue_name)
    if res:
        rm_first(redis_cli, queue_name)
        return json.loads(res[0])
    return None


def list(queue_name):
    res = pull_all(redis_cli, queue_name)
    if res:
        res = [json.loads(i) for i in res]
        return res
    return None


def create(queue_name, item):
    publish(redis_cli, queue_name, item)


def rm(queue_name):
    rm_first(redis_cli, queue_name)


def rm_index(queue_name, ind):
    rm_at(redis_cli, queue_name, ind)


def clear():
    clear_all(redis_cli)

from redis import StrictRedis
import json


def publish(redis_cli: StrictRedis, queue_name: str, item: dict):
    redis_cli.rpush(queue_name, json.dumps(item))


def pull(redis_cli: StrictRedis, queue_name: str):
    return redis_cli.lrange(queue_name, 0, 0)


def pull_all(redis_cli: StrictRedis, queue_name: str):
    return redis_cli.lrange(queue_name, 0, -1)


def rm_first(redis_cli: StrictRedis, queue_name: str):
    redis_cli.ltrim(queue_name, 1, -1)


def rm_at(redis_cli: StrictRedis, queue_name: str, index: int):
    deleted = '{"item": "DELETED"}'
    redis_cli.lset(queue_name, index, deleted)
    redis_cli.lrem(queue_name, 1, deleted)


def clear_all(redis_cli: StrictRedis):
    redis_cli.flushall()

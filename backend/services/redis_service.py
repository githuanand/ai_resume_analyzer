import os
import redis


REDIS_HOST = os.getenv(
    "REDIS_HOST",
    "localhost"
)

REDIS_PORT = int(
    os.getenv(
        "REDIS_PORT",
        6379
    )
)


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True
)


def test_redis():

    redis_client.set(
        "test_key",
        "hello_redis"
    )

    return redis_client.get(
        "test_key"
    )
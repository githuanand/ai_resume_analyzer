import redis


redis_client = redis.Redis(
    host="redis",
    port=6379,
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
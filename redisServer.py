import redis
import os

redis_server = redis.from_url(os.environ.get("REDIS_URL"))
env_table = 'env_table'


def setEnvVariable(message):
    message_list = message.split(' ')
    envKey = str(message_list[1])
    envValue = str(message_list[2])

    redis_server.hset(env_table, envKey, envValue)

    return "done"

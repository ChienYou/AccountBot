import json

import redis
import os

redis_server = redis.from_url(os.environ.get("REDIS_URL"))
env_table = 'env_table'


def setEnvVariable(user_id, message):

    message_list = message.split(' ')
    envKey = str(message_list[1])
    envValue = str(message_list[2])

    db_value = redis_server.hget(env_table, user_id) or '{}'

    db_json = json.loads(db_value)
    db_json[envKey] = envValue
    json_string = json.dumps(db_json)

    redis_server.hset(env_table, user_id, json_string)

    return "done"

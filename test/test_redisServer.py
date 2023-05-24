import redis

redis_server = redis.Redis(host='127.0.0.1', port='6379')


def setToken():
    redis_server.hset('Test', 'token', 'test')
    token = redis_server.hget('Test', 'token')
    print(token)


setToken()

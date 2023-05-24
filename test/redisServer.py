import redis

redis_server = redis.Redis()


def setToken():
    res = redis_server.set('Token', 'test')
    print(res)
    token = redis_server.get('Token')
    print(token)


setToken()
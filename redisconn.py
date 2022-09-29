import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0)

def save(data):
    return r.set(data['transaction'], json.dumps(data), ex=7*24*60*60)

def remove(transaction):
    return r.delete(transaction)

def read(transaction):
    data = r.get(transaction)
    return json.loads(data) if data is not None else None


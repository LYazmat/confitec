import redis
import json

# Using default to create a connect
r = redis.Redis(host='localhost', port=6379, db=0)

# Redis (key, data) => (transaction_id, response_data_string)

def save(data):
    # dumps artist response, expire in 7 days (convert to seconds)
    return r.set(data['transaction'], json.dumps(data), ex=7*24*60*60)

def remove(transaction):
    return r.delete(transaction)

def read(transaction):
    data = r.get(transaction)
    return json.loads(data) if data is not None else None


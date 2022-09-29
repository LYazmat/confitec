#
# Just testing functions from controller
# Check if it's respecting cache parameter and caching in Redis
#

from controller import read_from_artist
import redisconn
import random

# Test: find artist and save in Redis (cache=True)

def test_controller_artist_cache():
    id = random.randint(1, 10000)
    artist = read_from_artist(id=id, cache=True)
    if 'id' in artist:
        cache = redisconn.read(artist['transaction'])
        assert artist['transaction'] == cache['transaction']
    else:
        assert artist['msg'] == 'Artist not found'

# Test: find artist and don't save or remove key from Redis (cache=False)

def test_controller_artist_not_cache():
    id = random.randint(1, 10000)
    artist = read_from_artist(id=id, cache=False)
    if 'id' in artist:
        cache = redisconn.read(artist['transaction'])
        assert cache is None
    else:
        assert artist['msg'] == 'Artist not found'

# Test: return data direct from Redis (is cached)

def test_controller_artist_is_cached():
    artist = read_from_artist(id=750, cache=True)
    artist = read_from_artist(id=750, cache=True)
    if 'id' in artist:
        assert artist['from_cache'] is True
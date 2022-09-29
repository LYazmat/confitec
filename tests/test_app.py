#
# Just testing requests and json responses
#

def test_request_test(client):
    assert client.get("/test").get_json() == {'msg': 'Test successful'}

def test_request_not_found(client):
    assert client.get("/anything").get_json() == {'msg': 'Not a valid url'}
    assert client.get("/artist/aa").get_json() == {'msg': 'Not a valid url'}

def test_request_root(client):
    assert client.get('/').get_json()["msg"] in ['Table already exists', 'Table created']

def test_request_artist_not_found(client):
    assert client.get('/artist/40').get_json() == {'msg': 'Artist not found'}

def test_found_some_artist(client):
    assert client.get('/artist/750').get_json()["id"] == 750

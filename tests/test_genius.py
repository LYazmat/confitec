#
# Just testing functions from external APIs
#

from genius import check_artist, get_top_songs_by_artist

def test_genius_not_found():
    # Artist[id] 40 does not exist in genius
    assert check_artist(40).status_code == 404

def test_genius_some_artist():
    # Artist[id] 750 has the name 'All City Chess Club' on 2022-09-29
    artist = check_artist(750)
    assert artist.status_code == 200
    assert artist.json()['response']['artist']['id'] == 750

def test_genius_get_top_songs_by_artist_not_found():
    artist = get_top_songs_by_artist('aaa')
    assert artist['id'] == None

def test_genius_get_top_songs_by_artist_found():
    artist = get_top_songs_by_artist('750')
    assert artist['id'] == 750
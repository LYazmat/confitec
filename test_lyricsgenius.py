from lyricsgenius import Genius
import json

token = 'EYCQMd05lpJaD_X7__1_9W3pn-wafkxLvgEAjjCVPbjvfq9fgjlem-zGE5Jp4qj_'

genius = Genius(token)

artist = genius.search_artist('Andy Shauf', max_songs=1)

songs = []

request = genius.artist_songs(artist.id, sort='popularity', per_page=10, page=1)

print(json.dumps(request))
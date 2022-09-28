import json
import requests

token = 'Bearer EYCQMd05lpJaD_X7__1_9W3pn-wafkxLvgEAjjCVPbjvfq9fgjlem-zGE5Jp4qj_'

headers = {'Authorization': f'{token}'}

url_artist = f'https://api.genius.com/artists/{45}'

response = requests.get(url_artist, headers=headers)

if response.status_code == 200:

    result = response.json()
    artist = result['response']['artist']
    print(artist['id'], artist['name'])

    url_songs = f'https://api.genius.com/artists/{45}/songs'    
    params = {'per_page': '10', 'page': '1'}

    response = requests.get(url_songs, headers=headers, params=params)

    result = response.json()
    [print(r['full_title']) for r in result['response']['songs']]

import requests
import config

# Bearer Token Authorization in Header
headers = {'Authorization': f'Bearer {config.CLIENT_ACCESS_TOKEN}'}

def check_artist(id):

    # Look artist data in Genius by id
    # For more details: https://docs.genius.com

    # First search for artist
    url_artist = f'https://api.genius.com/artists/{id}'
    
    return requests.get(url_artist, headers=headers)


def get_top_songs_by_artist(id):

    response = check_artist(id)

    # Check artist response
    if response.status_code == 200:

        result = response.json()
        artist = result['response']['artist']

        # Check for top 10 songs, default sort is popularity attr
        url_songs = f'https://api.genius.com/artists/{id}/songs'    
        params = {'per_page': '10', 'page': '1'}
        response = requests.get(url_songs, headers=headers, params=params)
        result = response.json()

        return {
            'id': artist['id'], 'name': artist['name'],
            'songs': [r['full_title'] for r in result['response']['songs']]
        }

    else:      
        return {
            'id': None,
            'msg': 'Something wrong happened',
            'response': response.json()
        }
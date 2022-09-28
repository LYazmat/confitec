from flask import Flask, request
from controller import ArtistModel

app = Flask(__name__)


@app.route('/test')
def test():
    return {
        'msg': 'Test successful'
    }

@app.route('/')
def root_route(): 
    return ArtistModel().create_table_artists()


@app.route('/artist/<int:id>', methods=['GET'])
def get_artist(id):
    cache = request.args.get('cache') != 'False'
    response = ArtistModel().read_from_artist(id, cache)
    return response


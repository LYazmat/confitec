from flask import Flask, request
import controller

def create_app():

    app = Flask(__name__)

    @app.route('/test')
    def test():
        return {
            'msg': 'Test successful'
        }

    @app.route('/')
    def root_route(): 
        return controller.create_table_artists()

    @app.route('/artist/<int:id>', methods=['GET'])
    def get_artist(id):
        cache = request.args.get('cache') != 'False'
        response = controller.read_from_artist(id, cache)
        return response

    @app.route('/<path:path>')
    def catch_all(path):
        return {
            'msg': 'Not a valid url'
        }

    return app

create_app()
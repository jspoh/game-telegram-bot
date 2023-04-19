from flask import Blueprint, make_response, request

homeBp = Blueprint('home', __name__)


@homeBp.route('/', methods=['GET'])
def get():
    availablePaths = [
        {'path': '/', 'methods': ['GET', 'POST'], 'subpaths': ['/']},
        {'path': '/cw', 'methods': ['GET'], 'subpaths': [
            '/', '/wdls-to-jb', '/wdls-to-bke', '/view-from-tuas', '/tuas-second-link']},
        {'path': '/datetime', 'methods': ['GET'], 'subpaths': ['/']},
        {'path': '/game', 'methods': ['GET'], 'subpaths': [
            '/tod/t', '/tod/d', '/paranoia', '/nhie']},
    ]
    return make_response({'active': True, 'paths': availablePaths}, 200)


@homeBp.route('/', methods=['POST'])
def post():
    body = request.get_json()
    print(body)
    return make_response({'status': 'success'}, 201)

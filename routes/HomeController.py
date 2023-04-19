from flask import Blueprint, make_response, request

homeBp = Blueprint('home', __name__)


@homeBp.route('/', methods=['GET'])
def get():
    return make_response({'active': True}, 200)


@homeBp.route('/', methods=['POST'])
def post():
    body = request.get_json()
    print(body)
    return make_response({'status': 'success'}, 201)

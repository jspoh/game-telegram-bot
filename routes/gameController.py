from flask import Blueprint, make_response
import requests

gameBp = Blueprint('game', __name__)


@gameBp.route('/<game>', defaults={'option': None}, methods=['GET'])
@gameBp.route('/<game>/<option>', methods=['GET'])
def gameHandler(game: str, option: str):
    if game == 'tod' or game == 'truth-or-dare':
        if option == 't' or option == 'truth':
            truth = requests.get(
                'https://api.truthordarebot.xyz/v1/truth').json()['question']
            return {'data': truth}
        elif option == 'd' or option == 'dare':
            dare = requests.get(
                'https://api.truthordarebot.xyz/api/dare').json()['question']
            return {'data': dare}

    elif game == 'nhie' or game == 'never-have-i-ever':
        msg = requests.get(
            'https://api.truthordarebot.xyz/api/nhie').json()['question']
        return {'data': (msg)}

    elif game == 'paranoia':
        msg = requests.get(
            'https://api.truthordarebot.xyz/api/paranoia').json()['question']
        return {'data': msg}

    elif game == 'wyr' or game == 'would-you-rather':
        msg = requests.get(
            'https://api.truthordarebot.xyz/api/wyr').json()['question']
        return {'data': msg}

    else:
        return make_response({'error': f'Game {game} does not exist'}, 400)

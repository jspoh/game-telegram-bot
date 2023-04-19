from flask import Flask, request, make_response
import requests
import datetime
from causewayCameras import CausewayCameras
# import sqlalchemy as db

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get():
    return make_response({'active': True}, 200)


'''
fetch('/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({test: true})
            }
     )
'''


@app.route('/', methods=['POST'])
def post():
    body = request.get_json()
    print(body)
    return make_response({'status': 'success'}, 201)


@app.route('/cw', defaults={'camera': None}, methods=['GET'])
@app.route('/cw/<camera>', methods=['GET'])
def getCauseway(camera: str):
    # query = request.args.get('q')

    cwCctv = CausewayCameras()
    cwCctv.init()

    if not camera:
        data = cwCctv.all_cameras()
        cwCctv.close_driver()
        return {'data': data}

    # match camera:
    #     case 'wdls-to-jb':
    #         data = cwCctv.wdls_to_jb()
    #         cwCctv.close_driver()
    #         return {'data': data}
    #     case 'wdls-to-bke':
    #         data = cwCctv.wdls_to_bke()
    #         cwCctv.close_driver()
    #         return {'data': data}
    #     case 'view-from-tuas':
    #         data = cwCctv.view_from_tuas()
    #         cwCctv.close_driver()
    #         return {'data': data}
    #     case 'tuas-second-link':
    #         data = cwCctv.tuas_second_link()
    #         cwCctv.close_driver()
    #         return {'data': data}
    #     case _:
    #         cwCctv.close_driver()
    #         return (make_response(
    #             {'error': 'Bad request, {} does not exist'.format(camera)}, 400))

    if camera == 'wdls-to-jb':
        data = cwCctv.wdls_to_jb()
        cwCctv.close_driver()
        return {'data': data}
    elif camera == 'wdls-to-bke':
        data = cwCctv.wdls_to_bke()
        cwCctv.close_driver()
        return {'data': data}
    elif camera == 'view-from-tuas':
        data = cwCctv.view_from_tuas()
        cwCctv.close_driver()
        return {'data': data}
    elif camera == 'tuas-second-link':
        data = cwCctv.tuas_second_link()
        cwCctv.close_driver()
        return {'data': data}
    else:
        cwCctv.close_driver()
        return (make_response(
            {'error': f'Bad request, {camera} does not exist'}, 400))


@app.route('/datetime')
def getDatetime():
    return {'data': datetime.datetime.now()}


@app.route('/game/<game>', defaults={'option': None}, methods=['GET'])
@app.route('/game/<game>/<option>', methods=['GET'])
def gameHandler(game: str, option: str):
    '''
    match game:
        case 'tod' | 'truth-or-dare':
            match option:
                case 't' | 'truth':
                    truth = requests.get(
                        'https://api.truthordarebot.xyz/v1/truth').json()['question']
                    return {'data': (truth)}
                case 'd' | 'dare':
                    dare = requests.get(
                        'https://api.truthordarebot.xyz/api/dare').json()['question']
                    return {'data': (dare)}
        case 'nhie' | 'never-have-i-ever':
            msg = requests.get(
                'https://api.truthordarebot.xyz/api/nhie').json()['question']
            return {'data': (msg)}
    '''

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


def main():
    app.run(debug=True)


if __name__ == '__main__':
    pass
    # main()

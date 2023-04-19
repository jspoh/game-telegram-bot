from flask import Flask, request, make_response
import requests
import datetime
from util.causewayCameras import CausewayCameras
import sqlalchemy as db

app = Flask(__name__)
cwCctv = CausewayCameras()


def main():
    app.run(debug=True)


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

    cwCctv.init()
    if not camera:
        cwCctv.close_driver()
        return {'data': cwCctv.all_cameras()}

    # rewrite match statement since vercel does not support 3.10 syntax
    '''
    match camera:
        case 'wdls-to-jb':
            cwCctv.close_driver()
            return {'data': (cwCctv.wdls_to_jb())}
        case 'wdls-to-bke':
            cwCctv.close_driver()
            return {'data': (cwCctv.wdls_to_bke())}
        case 'view-from-tuas':
            cwCctv.close_driver()
            return {'data': (cwCctv.view_from_tuas())}
        case 'tuas-second-link':
            cwCctv.close_driver()
            return {'data': (cwCctv.tuas_second_link())}
        case _:
            cwCctv.close_driver()
            return {'data': (make_response(
                {'error': 'Bad request, {} does not exist'.format(camera)}, 400))}
    '''

    if camera == 'wdls-to-jb':
        cwCctv.close_driver()
        return {'data': (cwCctv.wdls_to_jb())}
    elif camera == 'wdls-to-bke':
        cwCctv.close_driver()
        return {'data': (cwCctv.wdls_to_bke())}
    elif camera == 'view-from-tuas':
        cwCctv.close_driver()
        return {'data': (cwCctv.view_from_tuas())}
    elif camera == 'tuas-second-link':
        cwCctv.close_driver()
        return {'data': (cwCctv.tuas_second_link())}
    else:
        cwCctv.close_driver()
        return {'data': (make_response(
            {'error': 'Bad request, {} does not exist'.format(camera)}, 400))}


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
            return {'data': (truth)}
        elif option == 'd' or option == 'dare':
            dare = requests.get(
                'https://api.truthordarebot.xyz/api/dare').json()['question']
            return {'data': (dare)}

    elif game == 'nhie' or game == 'never-have-i-ever':
        msg = requests.get(
            'https://api.truthordarebot.xyz/api/nhie').json()['question']
        return {'data': (msg)}


if __name__ == '__main__':
    main()

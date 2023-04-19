from flask import Blueprint, make_response, request
from api.causewayCameras.CausewayCameras import CausewayCameras

causewayBp = Blueprint('cw', __name__)


@causewayBp.route('/cw', defaults={'camera': None}, methods=['GET'])
@causewayBp.route('/cw/<camera>', methods=['GET'])
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

from flask import Blueprint
import datetime

datetimeBp = Blueprint('datetime', __name__)


@datetimeBp.route('/datetime')
def getDatetime():
    return {'data': datetime.datetime.now()}

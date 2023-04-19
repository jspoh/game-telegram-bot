from flask import Blueprint
import datetime

datetimeBp = Blueprint('datetime', __name__)


@datetimeBp.route('/')
def getDatetime():
    return {'data': datetime.datetime.now()}

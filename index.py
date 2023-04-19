from flask import Flask

from routes.HomeController import homeBp
from routes.cwController import causewayBp
from routes.datetimeController import datetimeBp
from routes.gameController import gameBp

app = Flask(__name__)

app.register_blueprint(homeBp)
app.register_blueprint(causewayBp, url_prefix='/cw')
app.register_blueprint(datetimeBp, url_prefix='/datetime')
app.register_blueprint(gameBp, url_prefix='/game')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    pass
    # main()

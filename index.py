from flask import Flask

from routes.HomeController import homeBp
from routes.cwController import causewayBp
from routes.datetimeController import datetimeBp
from routes.gameController import gameBp

app = Flask(__name__)

app.register_blueprint(homeBp)
app.register_blueprint(causewayBp)
app.register_blueprint(datetimeBp)
app.register_blueprint(gameBp)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    pass
    main()

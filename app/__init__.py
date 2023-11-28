import json

from flask import Flask
from flask_socketio import SocketIO

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://nukeops.com",
]

socketio = SocketIO(cors_allowed_origins=origins)

with open("config.json") as config:
    conf = json.loads(config.read())


def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.config["SECRET_KEY"] = conf.get("secret_key", "some very secret key")

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app

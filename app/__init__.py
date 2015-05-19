__author__ = 'jonathan'

from flask import Flask
from flask.ext.socketio import SocketIO

socketio = SocketIO()


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

    from .server import server as main_blueprint
    app.register_blueprint(main_blueprint)

    socketio.init_app(app)
    return app


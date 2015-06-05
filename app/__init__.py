__author__ = 'jonathan'

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.socketio import SocketIO

app = Flask(__name__)
app.config.from_pyfile('_config.py')
db = SQLAlchemy(app)
socketio = SocketIO(app)

from app.users.views import users_blueprint

app.register_blueprint(users_blueprint)

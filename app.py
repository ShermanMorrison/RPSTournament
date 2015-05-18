__author__ = 'jonathan'

from gevent import monkey
from flask import Flask, Response, render_template, request, redirect, url_for
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

monkey.patch_all()

#configuration
application = Flask(__name__)
application.debug = True
application.config['PORT'] = 5000

#routing

@application.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print "Got log in request from " + request.form['username']
        print "with password " + request.form['password']
        return redirect(url_for('lobby'))
    else:
        return render_template('login.html')

@application.route('/lobby')
def lobby():
    print "in lobby"
    return render_template('lobby.html')

@application.route('/game')
def game():
    return render_template('game.html')
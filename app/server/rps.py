__author__ = 'jonathan'

from flask import render_template, request, redirect, url_for, session, flash
from . import server
from .. import socketio
from functools import wraps

users = []
#routing
@server.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # pop old username for this client
        session.pop('name', None)

        # make new username for this client
        session['name'] = request.form['username']
        # users.append(session['name'])

        return redirect(url_for('.lobby'))
    else:
        return render_template('login.html')


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'name' in session:
            return test(*args, **kwargs)
        else:
            flash('You must log in to view this page')
            return redirect(url_for('.login'))
    return wrap


@server.route('/lobby')
@login_required
def lobby():


    print "in lobby"
    name = session['name']
    return render_template('lobby.html', name=name, users=users)


@server.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    if request.method == 'POST':
        move = request.form['data']
        sender = request.form['sender']
        socketio.emit('submittedMove', {'msg': move, 'sender': sender}, namespace='/game')
        print "got post request for game submit move"
        return 'Received'

    name = session['name']
    return render_template('game.html', name=name)

@socketio.on('connect', namespace='/game')
def connect():
    global users
    try:
        if 'name' in session:
            session.pop('name')
        users.append(session['name'])
        socketio.emit('joined', {'sender': session['name']}, namespace='/game')
    except ValueError:
        pass
    # pass

@socketio.on('disconnect', namespace='/game')
def disconnect():
    global users
    if 'name' in session:
        # emit leave message to all clients
        if session['name'] in users:
            users.remove(session['name'])
            socketio.emit('left', {'sender': session['name']}, namespace='/game')



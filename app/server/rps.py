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
        if 'name' in session:
            try:
                users.remove(session['name'])
            except ValueError:
                pass
        session.pop('name', None)

        # make new username for this client
        session['name'] = request.form['username']
        if session['name'] not in users:
            users.append(session['name'])

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
    socketio.emit('status', {'msg': 'you have entered the room'}, broadcast=True)
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
    # try:
    #     users.append(session['name'])
    # except ValueError:
    #     pass
    pass

@socketio.on('disconnect', namespace='/game')
def disconnect():
    # pass
    if 'name' in session:
        try:
            users.remove(session['name'])
        except ValueError:
            pass
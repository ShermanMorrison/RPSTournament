__author__ = 'jonathan'

from flask import render_template, request, redirect, url_for, session, flash
from . import server
from .. import socketio
from flask.ext.socketio import join_room, leave_room
from functools import wraps
from uuid import uuid4

users = {}
rooms = []
#routing
@server.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # pop old username for this client
        session.pop('name', None)

        # make new username for this client
        session['name'] = request.form['username']
        session['room'] = request.form['username']

        #make uuid for session
        session['uuid'] = str(uuid4())

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


@server.route('/lobby', methods=['GET', 'POST'])
@login_required
def lobby():
    if request.method == 'POST':
        if request.form['type'] == 'challenge':
            target = request.form['target']
            socketio.emit('challengeRequest', {'target': target, 'sender': session['room']}, namespace='/game', room=target)
            return "Sent challengeRequest"
        elif request.form['type'] == 'challengeResponse':
            #send accept message to target
            socketio.emit('challengeResponse', {'response': request.form['response']}, namespace='/game', room=request.form['challenger'])
            return "Sent accept"

    print "in lobby"
    name = session['name']
    session['room'] = session['name']
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

    join_room(session['room'])
    # socketio.emit('challengeRequest', {'target': session['room'], 'sender': session['room']}, namespace='/game', room=session['room'])
    try:
        if session['uuid'] not in users:
            users[session['uuid']] = [session['name']]
        else:
            users[session['uuid']].append(session['name'])
        socketio.emit('joined', {'sender': session['name']}, namespace='/game')
    except ValueError:
        pass
    # pass

@socketio.on('disconnect', namespace='/game')
def disconnect():
    global users
    if 'name' in session:
        # emit leave message to all clients
        try:
            users[session['uuid']].pop(0)
            socketio.emit('left', {'sender': session['name']}, namespace='/game')
        except ValueError:
            pass




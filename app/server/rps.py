__author__ = 'jonathan'

from flask import render_template, request, redirect, url_for, session, flash
from . import server
from .. import socketio
from flask.ext.socketio import join_room, leave_room
from functools import wraps
from uuid import uuid4

users = {}
rooms = []
games = {}
inGameSessions = {}

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

def inGame_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'inGame' in session:
            return test(*args, **kwargs)
        else:
            flash('You must be in a game to view this page')
            if 'name' in session:
                return redirect(url_for('.lobby'))
            else:
                return redirect(url_for('.login'))
    return wrap


@server.route('/lobby', methods=['GET', 'POST'])
@login_required
def lobby():
    if request.method == 'POST':
        if request.form['type'] == 'challenge':
            target = request.form['target']
            socketio.emit('challengeRequest', {'target': target, 'sender': session['room']}, namespace='/game', room=target)
            session['challenger'] = session['name']
            session['challengee'] = session[target]
            return "Sent challengeRequest"
        elif request.form['type'] == 'challengeResponse':
            # 1 session enters here
            # send challenge response to sender and target
            session['challenger'] = request.form['challenger']
            session['challengee'] = session['name']
            games[session['challenger']] = {'challenger': -1, 'challengee': -1}
            socketio.emit('challengeResponse', {'response': request.form['response']}, namespace='/game', room=request.form['challenger'])
            socketio.emit('challengeResponse', {'response': request.form['response']}, namespace='/game', room=session['name'])
            return "Sent challengeResponse's"
        elif request.form['type'] == 'joinGame':
            # 2 sessions enter here
            # make a game entry
            session['inGame'] = True
            socketio.emit('joinGame', {}, namespace='/game', room=session['name'])
            return "Sent joinGame"

    print "in lobby"
    name = session['name']
    session['room'] = session['name']
    return render_template('lobby.html', name=name, users=users)


@server.route('/game', methods=['GET', 'POST'])
@inGame_required
def game():
    global session
    if request.method == 'POST':
        move = request.form['data']
        sender = request.form['sender']
        if sender == session['challenger']:
            submitter = 'challenger'
        else:
            submitter = 'challengee'
        if -1 in games[session['challenger']].values():
            games[session['challenger']][submitter] = move
        else:
            games[session['challenger']][submitter] = move
            socketio.emit('submittedMove', {'msg': games[session['challenger']][submitter], 'sender': sender}, room=session['challenger'])
            socketio.emit('submittedMove', {'msg': games[session['challengee']][submitter], 'sender': sender}, room=session['challengee'])
        print "got post request for game submit move"
        return 'Received'

    name = session['name']
    return render_template('game.html', name=name)

@socketio.on('connect', namespace='/game')
def connect():
    global users

    join_room(session['room'])
    try:
        if session['uuid'] not in users:
            users[session['uuid']] = [session['name']]
        else:
            users[session['uuid']].append(session['name'])
        socketio.emit('joined', {'sender': session['name']}, namespace='/game')
    except ValueError:
        pass

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




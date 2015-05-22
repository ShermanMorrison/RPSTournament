__author__ = 'jonathan'

from flask import render_template, request, redirect, url_for, session
from . import server
from .. import socketio

#routing
@server.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print "Got log in request from " + request.form['username']
        print "with password " + request.form['password']
        session['name'] = request.form['username']
        return redirect(url_for('.lobby'))
    else:
        return render_template('login.html')


@server.route('/lobby')
def lobby():
    socketio.emit('status', {'msg': 'you have entered the room'}, broadcast=True)
    print "in lobby"
    name = session['name']
    return render_template('lobby.html', name=name)


@server.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        move = request.form['data']
        sender = request.form['sender']
        socketio.emit('submittedMove', {'msg': move, 'sender': sender}, namespace='/game')
        print "got post request for game submit move"
        return 'Received'

    name = session['name']
    return render_template('game.html', name=name)

@socketio.on('text', namespace='/game')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    socketio.emit('submittedMove', {'msg': 0}, namespace='/game', broadcast=True)

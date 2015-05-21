__author__ = 'jonathan'

from flask import render_template, request, redirect, url_for
from . import server
from .. import socketio

#routing
@server.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print "Got log in request from " + request.form['username']
        print "with password " + request.form['password']
        return redirect(url_for('.lobby'))
    else:
        return render_template('login.html')


@server.route('/lobby')
def lobby():
    socketio.emit('status', {'msg': 'you have entered the room'}, broadcast=True)
    print "in lobby"
    return render_template('lobby.html')


@server.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        move = request.form['data']
        socketio.emit('submittedMove', {'msg': move}, namespace='/game')
        print "got post request for game submit move"
        return 'Received'
    return render_template('game.html')

@socketio.on('text', namespace='/game')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    socketio.emit('submittedMove', {'msg': 0}, namespace='/game', broadcast=True)

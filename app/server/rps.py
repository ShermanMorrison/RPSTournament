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
        return render_template('chat.html')


@server.route('/lobby')
def lobby():
    socketio.emit('status', {'msg': 'you have entered the room'}, broadcast=True)
    print "in lobby"
    return render_template('lobby.html')


@server.route('/game', methods=['GET', 'POST'])
def game():
    return render_template('game.html')

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    pass

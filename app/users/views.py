__author__ = 'jonathan'

#############
#  imports  #
#############

from flask import render_template, request, redirect, url_for, \
    session, flash, Blueprint
from functools import wraps
from sqlalchemy.exc import IntegrityError

from app import db
from app import socketio
from flask.ext.socketio import join_room, leave_room
from app.models import User

##############
#   config   #
##############

users_blueprint = Blueprint('users', __name__)

users = {}
rooms = []
games = {}
inGameSessions = {}


###############
#   helpers   #
###############

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
        game_id = kwargs['game_id']
        print game_id
        print session
        if game_id in session:
            return test(*args, **kwargs)
        else:
            flash('You must be in a game to view this page')
            if 'name' in session:
                return redirect(url_for('.lobby'))
            else:
                return redirect(url_for('.login'))
    return wrap


##############
#   routes   #
##############
@users_blueprint.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        # query for user in database
        user = db.session.query(User) \
            .filter_by(name=request.form['username']).first()

        # if user in db and password is correct, login
        if user is not None and user.password == request.form['password']:
            session['logged_in'] = True
            session['user_id'] = user.id
            session['name'] = user.name
            return redirect(url_for('users.lobby'))
        else:
            error = "Invalid username or password."

    return render_template('login.html', error=error)


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        new_user = User(
            request.form['username'],
            request.form['password']
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Thanks for registering, ' + request.form['username'] + '. Please log in.')
        except IntegrityError:
            error = 'That username and/or email already exists'
            return render_template('register.html', error=error)

    return render_template('register.html', error=error)



@users_blueprint.route('/lobby', methods=['GET', 'POST'])
@login_required
def lobby():
    if request.method == 'POST':
        name = session['name']
        if request.form['type'] == 'leaveLobby':
            print "Leaving lobby: Removing user!"
            if len(users[session['user_id']]) == 1:
                users.pop(session['user_id'], None)
            else:
                users[session['user_id']].remove(session['name'])
            print('post to lobby')
            return render_template('lobby.html', name=name, users=users)
        elif request.form['type'] == 'challenge':
            target = request.form['target']
            socketio.emit('challengeRequest', {'target': target, 'sender': session['name']}, namespace='/game', room=target)
            return render_template('lobby.html', name=name, users=users, target=target)
        elif request.form['type'] == 'challengeAccept':
            challenger = request.form['challenger']
            challengee = session['name']
            games[challenger] = {'challenger': -1, 'challengee': -1}
            socketio.emit('challengeAccept', {'challenger': challenger,
                                              'challengee': challengee},
                          namespace='/game', room=challenger)
            socketio.emit('challengeAccept', {'challenger': challenger,
                                              'challengee': challengee},
                          namespace='/game', room=challengee)
            return "Sent challengeResponse's"
        elif request.form['type'] == 'challengeDecline':

            challenger = request.form['challenger']
            print "declining challenge from " + str(challenger)
            socketio.emit('challengeDecline', {}, namespace='/game', room=challenger)
            return "Declined  challenge from " + str(challenger)
        elif request.form['type'] == 'challengeCancel':
            challengee = request.form['challengee']
            print "cancelling challenge to " + str(challengee)
            socketio.emit('challengeCancel', {}, namespace='/game', room=challengee)
            return "cancelled challenge to " + str(challengee)
        elif request.form['type'] == 'joinGame':
            challenger = request.form['challenger']
            challengee = request.form['challengee']
            session['challenger'] = request.form['challenger']
            session['challengee'] = request.form['challengee']
            print session['challenger']
            print session['challengee']
            session['inGame'] = True

            print "HERE"
            if session['name'] == challenger:
                role = 'challenger'
            else:
                role = 'challengee'

            print "WOOO HEREEE"
            game_id = challenger + "/" + challengee
            print "WOOOW COWBOY!"
            print game_id
            print role
            session[str(game_id)] = role

            print "GOOOOAALLL HEREEE"
            socketio.emit('joinGame', {'game_id': game_id}, namespace='/game', room=session['name'])
            return "Sent joinGame"
    else:
        print('get to lobby: Adding user!')
        name = session['name']
        if session['user_id'] not in users:
            users[session['user_id']] = [session['name']]
        else:
            users[session['user_id']].append(session['name'])
        print users[session['user_id']]
        return render_template('lobby.html', name=name, users=users)


@users_blueprint.route('/game/<path:game_id>', methods=['GET', 'POST'])
@inGame_required
def game(game_id):
    name = session['name']
    print name
    # session.pop('inGame', None)

    if request.method == 'POST':
        move = request.form['data']
        sender = request.form['sender']
        print move
        print sender
        print session['challenger']
        print games
        print session['challenger'] in games
        if sender == session['challenger']:
            submitter = 'challenger'
        else:
            submitter = 'challengee'

        if -2 == sum(move for move in games[session['challenger']].values() if move == -1):
            games[session['challenger']][submitter] = move
        else:
            print "here!!"
            print submitter
            games[session['challenger']][submitter] = move
            print games[session['challenger']]
            print session['challenger']
            print session['challengee']
            socketio.emit('submittedMove', {'msg': games[session['challenger']]['challengee'], 'sender': session['challengee']}, namespace='/game', room=session['challenger'])
            socketio.emit('submittedMove', {'msg': games[session['challenger']]['challenger'], 'sender': session['challenger']}, namespace='/game', room=session['challengee'])
            games[session['challenger']] = {'challenger': -1, 'challengee': -1}
        print "got post request for game submit move"
        print games[session['challenger']]
        return 'Received'

    return render_template('game.html', name=name, game_id=game_id)

@socketio.on('connect', namespace='/game')
def connect():
    global users
    print "User connected!"
    join_room(session['name'])

@socketio.on('disconnect', namespace='/game')
def disconnect():
    global users
    """
    if 'name' in session:
        # emit leave message to all clients
        try:
            users[session['user_id']].pop(0)
            socketio.emit('left', {'sender': session['name']}, namespace='/game')
        except ValueError:
            pass
    """











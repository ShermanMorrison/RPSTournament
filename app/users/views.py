__author__ = 'jonathan'

#############
#  imports  #
#############

from flask import render_template, request, redirect, url_for, \
session, flash, Blueprint
from uuid import uuid4
from functools import wraps
from sqlalchemy.exc import IntegrityError

from app import db
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
        if 'inGame' in session:
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
        if len(users[session['user_id']]) == 1:
            users.pop(session['user_id'], None)
        else:
            users[session['user_id']].remove(session['name'])
        name = session['name']
        print('post to lobby')
        return render_template('lobby.html', name=name, users=users)
    else:
        print('get to lobby')
        name = session['name']
        session['room'] = session['name']
        if session['user_id'] not in users:
            users[session['user_id']] = [session['name']]
        else:
            users[session['user_id']].append(session['name'])
        return render_template('lobby.html', name=name, users=users)















import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from ResumeWebsite.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.hget('users', username) is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            user_id = str(g.db.incrby('next_user_id', 1000))
            g.db.hmset('user:' + user_id, dict(username=username, password=password))
            g.db.hset('users', username, user_id)

            session['username'] = username

            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # db = get_db()
        error = None

        user_id = str(g.db.hget('users', username), 'utf-8')

        if not user_id:
            error = 'Incorrect username.'

        else:

            print("The password is " + password)

            saved_password = g.db.hget("user:2000", "password").decode('utf-8')
            print("Saved password is " + saved_password)

            if password != saved_password:
                print("caught error")
                error = 'Incorrect password'

            if error is None:
                session.clear()
                session['user_id'] = user_id
                session['username'] = username
                print("redirecting")
                return redirect(url_for('blog.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().hget('users', user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        #g.user = get_db().execute(
        #    'SELECT * FROM user WHERE id = ?', (user_id,)
        #).fetchone()


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # ensure StorageApp is online
        pass

        error = None

        # find username in the database
        #user = db.execute(
        #    'SELECT * FROM user WHERE username = ?', (username,)
        #).fetchone()

        # handle if user was not recognised
        #if user is None:
        #    error = 'Incorrect username.'
        #elif not check_password_hash(user['qpassword'], password):
        #    error = 'Incorrect password.'

        # start session if all good
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('client_main'))

        flash(error)

    return render_template('auth/login.html')
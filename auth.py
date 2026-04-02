from functools import wraps

from dotenv import load_dotenv
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

import os


def login_required_simple(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return wrapper

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        load_dotenv()
        password = request.form.get('password')
        PASSWORD_HASH = os.getenv("HASHED_PASS")
        print(PASSWORD_HASH)
        if PASSWORD_HASH and check_password_hash(PASSWORD_HASH, password):
            session['logged_in'] = True
            print("Login!")
            return redirect(url_for('main.stream'))
        else:
            print("BAD Login!")

            flash('Invalid password', 'error')

    return render_template('auth/login.html')

@auth.route('/logout')
# @login_required
def logout():
    # logout_user()
    session.pop('logged_in', None)
    return redirect(url_for('main.index'))

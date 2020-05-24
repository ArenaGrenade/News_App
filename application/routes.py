from flask import request, render_template, redirect, flash, url_for, session, g
from flask import current_app as app
from flask_login import login_required, logout_user, current_user, login_user
from .models import db, User
from . import news_api_client
from werkzeug.security import check_password_hash
from . import login_manager
import json


@app.route('/')
def homepage():
    return render_template("index.html");


@app.route('/register', methods=('GET', 'POST'))
def register():
    flag = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        flag = None

        if username is None:
            flag = 'Username is required.'
        elif password is None:
            flag = 'Password is required.'
        elif User.query.filter_by(username=username).first():
            flag = 'Username must be unique'
        elif User.query.filter_by(email=email).first():
            flag = 'Email is already registered'
        
        if flag:
            flash(flag)
        else:
            user = User(
                firstname=request.form['firstname'],
                lastname=request.form['lastname'],
                email=request.form['email'],
                username=request.form['username'],
                password=request.form['password']
            )
            db.session.add(user)
            db.session.commit()
            print('committed user to dbase')
            return redirect(url_for('login'))

    return render_template('auth/register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    flag = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user is None:
            flag = 'No such user'
        elif not check_password_hash(user.password, password):
            flag = 'Incorrect password'

        if flag:
            flash(flag)
        else:
            login_user(user)
            flash('Logged in')
            return redirect(url_for('test'))

    return render_template('auth/login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/test')
def test():
    return render_template('test.html')


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('User has to be logged in inorder to perform that action')
    return redirect(url_for('login'))


@app.route('/news_api_test')
def news_tester():
    headlines = news_api_client.get_top_headlines(language='en')
    return render_template('news_tester.html', articles=headlines['articles'])

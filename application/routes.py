from flask import request, render_template, redirect, flash, url_for, session, g
from flask import current_app as app
from .models import db, User
from . import news_api_client
from werkzeug.security import check_password_hash
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
            print('committed')


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
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('register'))

    return render_template('auth/login.html')


@app.before_request
def things_to_do():
    print('before request')
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        user = User.query.get(user_id)
        g.user = user
        print('user set')
        print(user)

@app.route('/news_api_test')
def news_tester():
    headlines = news_api_client.get_top_headlines(language='en')
    return render_template('news_tester.html', articles=headlines['articles'])

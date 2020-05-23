from flask import Flask, render_template, request, flash, redirect, url_for, session, g
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.secret_key = 'test'  # app.secret_key = 'a26d9e7eff0d4dba88d35458034c57b1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, '../dbase.sqlite')


# Import database and models
from models import db, User
db.init_app(app)

with app.app_context():
    db.create_all()


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
            return redirect(url_for('login'))
    
    if flag:
        flash(flag)
        print(flag)

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


if __name__ == '__main__':
    app.run(debug=True)

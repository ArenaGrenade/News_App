from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)
app.secret_key = 'test'  # app.secret_key = 'a26d9e7eff0d4dba88d35458034c57b1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, '../dbase.sqlite')


# Import database and models
from models import db, User
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
            return redirect(url_for('register'))  # Must redirect to login instead
    
    if flag:
        flash(flag)
        print(flag)

    return render_template('auth/register.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask import request, render_template, redirect, flash, url_for, session, g
from flask import current_app as app
from flask_login import login_required, logout_user, current_user, login_user
from .models import db, User, NewsArticle, Tag
from . import news_api_client
from werkzeug.security import check_password_hash
from . import login_manager
from datetime import datetime, timedelta


from newspaper import Article
import re
@app.route('/')
def homepage():
    return render_template("index.html")


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
                username=request.form['username'],
                password=request.form['password'],
                email=request.form['email']
            )
            db.session.add(user)
            db.session.commit()
            print('committed user to dbase')
            return redirect(url_for('login'))

    return render_template('register.html')


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

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('User has to be logged in inorder to perform that action')
    return redirect(url_for('login'))


#  TESTING METHODS
@app.route('/news_api_test')
def news_tester():
    time_now=datetime.now() - timedelta(hours=24)
    headlines = news_api_client.get_everything(language='en',
                                               sort_by='popularity',
                                               domains='bbc.co.uk',
                                               page_size=20,
                                               page=1,
                                               from_param=time_now.isoformat(timespec='seconds')
                                               )
    Article = headlines['articles']
    for article in Article:
        print(article['url'])
        print(article['publishedAt'])
        present = NewsArticle.query.filter_by(link=article['url']).first()
        if present is None:
            present = NewsArticle(
                date_published=article['publishedAt'],
                link=article['url'],
            )
            db.session.add(present)
            db.session.commit()
        article['news_id'] = present.id

    return render_template('news_tester.html',articles=Article)


# Parsed Data Here
@app.route('/<int:title>')
def ParsedData(title):
    print(type(title))
    quer=int(title)
    url=NewsArticle.query.get(quer).link
    print(url)
    article = Article(url)
    article.download()
    article.parse()
    print("Article Title:")
    print(article.title)
    print("Authors")
    print(article.authors)
    s = article.text
    paragraphs = re.split('\n\s*\n', s)
    Articledetails = {
        "Title":article.title,
        "Authors":article.authors,
        "Content":paragraphs
    }
    print(article.tags)
    return render_template("test/data.html",Variable=Articledetails)


@app.route('/newstest', methods=('GET', 'POST'))
def newstest():
    if request.method == 'POST':
        link = request.form['link']
        error = None

        if link is None:
            error = 'Link cannot be empty'
        elif NewsArticle.query.filter_by(link=link).first():
            error = 'Link needs to be unique'

        if error is None:
            article = NewsArticle(link=link)
            db.session.add(article)
            db.session.commit()

            return redirect(url_for('display'))
        flash(error)

    return render_template('test/newstest.html')


@app.route('/favorite_articles', methods=('GET', 'POST'))
@login_required
def favorite_articles():
    if request.method == 'POST':
        article_id = request.form['article_id']
        news_article = NewsArticle.query.get(article_id)
        user = User.query.get(current_user.id)

        if news_article is not None:
            print('retrieved ' + str(news_article.link))
            user.saved_articles.append(news_article)  #TODO: AttributeError: 'InstrumentedList' object has no attribute 'add'
            db.session.commit()
        else:
            print('Issue. No such article')

        print(user.saved_articles)
        return redirect((url_for('test')))
    return render_template('test/favorite_articles.html')


@app.route('/display_articles')
def display():
    news = NewsArticle.query.all()
    tags = Tag.query.all()
    return render_template('test/display_articles.html', articles=news, tags=tags)


# DO NOT REMOVE THIS PLEASE
@app.route('/test')
def test():
    articles = User.query.filter_by(id=current_user.id).first().saved_articles
    return render_template('test.html', articles=articles)


@app.route('/generate_tags')
def generate_tags():
    return redirect(url_for('test'))

@app.route('/home_page')
def home_page():
    return url_for('home.html')

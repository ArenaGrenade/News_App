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
    print(user.tags)
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
    user_save_list = []
    if current_user.is_authenticated:
        user_save_list = [article.id for article in User.query.filter_by(id=current_user.id).first().saved_articles]
    print(user_save_list)
    user_save_list = set(user_save_list)
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

        if present.id in user_save_list:
            article['saved'] = True
        else:
            article['saved'] = False

    #return render_template('news_tester.html',articles=Article)
    return render_template('news_tester_test.html', articles=Article)


@app.route('/tester')
def tester():
    headlines = news_api_client.get_top_headlines(language='en')['articles'][:5]
    print(headlines)
    return render_template('news_tester_test.html', headlines_all=headlines)


# Parsed Data Here
@app.route('/<int:title>')
def ParsedData(title):
    current_article = NewsArticle.query.get(title)
    url = current_article.link
    print('URL: ' + url + ' id ' + str(current_article.id))
    article = Article(url)
    article.download()
    article.parse()
    s = article.text
    paragraphs = re.split('\n\s*\n', s)

    saved_articles = []
    if current_user.is_authenticated:
        saved_articles = [article.id for article in User.query.filter_by(id=current_user.id).first().saved_articles]

    saved = False
    if title in saved_articles:
        saved = True

    print('This page has been saved ' + str(saved))
    article_details = {
        "Title": article.title,
        "Authors": article.authors,
        "Content": paragraphs,
        "id": current_article.id,
        "saved": saved
    }
    return render_template("test/data.html", Variable=article_details)


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
        article_id = request.form['data']
        operation = request.form['operation']
        news_article = NewsArticle.query.get(article_id)
        user = User.query.get(current_user.id)

        if news_article is not None:
            if operation == 'save':
                user.save_article(news_article)
            else:
                user.un_save_article(news_article)
            db.session.commit()
        else:
            print('Issue. No such article')

        return redirect(request.url)
    return render_template('test/favorite_articles.html')


# DO NOT REMOVE THIS PLEASE
@app.route('/test')
def test():
    articles = []
    if current_user.is_authenticated:
        articles = User.query.get(current_user.id).retrieve_articles()
    return render_template('test.html', articles=articles)


@app.route('/generate_tags')
def generate_tags():
    return redirect(url_for('test'))


@app.route('/home_page')
def home_page():
    return url_for('home.html')

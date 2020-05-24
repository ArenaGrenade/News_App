from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from newsapi import NewsApiClient
from config import NEWS_API_KEY
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
news_api_client = NewsApiClient(api_key=NEWS_API_KEY)


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    #  Attach application to modules
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()

        return app

import os

basedir = os.path.abspath(os.path.dirname(__file__))
NEWS_API_KEY = '78a80e3fd33f4c35ba74643024219cfd'


class Config:

    SECRET_KEY = 'test'
    FLASK_APP = 'app_runner.py'
    FLASK_DEBUG = 1

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '../dbase.sqlite')
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

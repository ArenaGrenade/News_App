import os

basedir = os.path.abspath(os.path.dirname(__file__))
NEWS_API_KEY = '78a80e3fd33f4c35ba74643024219cfd'


class Config:

    SECRET_KEY = 'b091yhcojm65ttn91vyc10cggynxmucyhcg0184cg08n1gc000gcn8gmyxg1yg48xg0874g7gcn8mgmxyg'
    FLASK_APP = 'app_runner.py'
    FLASK_DEBUG = 1
    project_dir = os.path.dirname(os.path.abspath(__file__))
    database_file = "sqlite:///{}".format(os.path.join(project_dir, "db.sqlite"))
    SQLALCHEMY_DATABASE_URI = database_file

    print(basedir)
    #SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

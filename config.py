import os

basedir = os.path.abspath(os.path.dirname(__file__))
NEWS_API_KEY = '78a80e3fd33f4c35ba74643024219cfd'


class Config:

    SECRET_KEY = 'b091yhcojm65ttn91vyc10cggynxmucyhcg0184cg08n1gc000gcn8gmyxg1yg48xg0874g7gcn8mgmxyg'
    FLASK_APP = 'app_runner.py'
    FLASK_DEBUG = 1

    SQLALCHEMY_DATABASE_URI = "postgres://xzrzrfnrggahbl:0f7aaeabcb50b45db2fd4b3086b08177e63723fd3bcf5bee83d0d997e54e9b83@ec2-34-198-243-120.compute-1.amazonaws.com:5432/ddk9876qjng4nt"
    print(basedir)
    #SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

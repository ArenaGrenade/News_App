import os

basedir = os.path.abspath(os.path.dirname(__file__))
NEWS_API_KEY = '78a80e3fd33f4c35ba74643024219cfd'


class Config:
    SECRET_KEY = 'b091yhcojm65ttn91vyc10cggynxmucyhcg0184cg08n1gc000gcn8gmyxg1yg48xg0874g7gcn8mgmxyg'
    FLASK_APP = 'app_runner.py'
    FLASK_DEBUG = 1

    SQLALCHEMY_DATABASE_URI = "postgres://yzuauynghmyjvr:7258bd70210a5d656b72fe8fae518f961504e728ede3ca727658c8fdae12ac5d@ec2-54-211-210-149.compute-1.amazonaws.com:5432/daktevo0cgdf4v"
    print(basedir)
    #SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

from . import db
from flask_sqlalchemy import event
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


association_table = db.Table('association',
                 db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                 db.Column('newsarticle_id', db.Integer, db.ForeignKey('newsarticle.id'), primary_key=True)
                 )

#
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     firstname = db.Column(db.String(24), nullable=False)
#     lastname = db.Column(db.String(24))
#     username = db.Column(db.String(24), unique=True, nullable=False)
#     password = db.Column(db.String(128), nullable=False)
#     email = db.Column(db.String(), unique=True, nullable=False)
#
#     saved_articles = db.relationship("NewsArticle", secondary=association_table)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(24), nullable=False)
    lastname = db.Column(db.String(24))
    username = db.Column(db.String(24), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)

    saved_articles = db.relationship("NewsArticle", secondary=association_table,
                                     backref=db.backref('newsarticles'))


@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value)
    return value


class NewsArticle(db.Model):
    __tablename__ = 'newsarticle'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link = db.Column(db.String(200), nullable=False)


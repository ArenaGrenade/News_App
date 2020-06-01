from . import db
from flask_sqlalchemy import event
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from sqlalchemy.ext.associationproxy import association_proxy


saved_articles = db.Table('association',
                          db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                          db.Column('newsarticle_id', db.Integer, db.ForeignKey('newsarticle.id'), primary_key=True)
                          )
related_tags = db.Table('related_tags',
                        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
                        db.Column('newsarticle_id', db.Integer, db.ForeignKey('newsarticle.id'), primary_key=True)
                        )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(24), nullable=False)
    lastname = db.Column(db.String(24))
    username = db.Column(db.String(24), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)

    saved_articles = db.relationship("NewsArticle", secondary=saved_articles,
                                     backref=db.backref('users'))

    tags = association_proxy('user_tags', 'tag',
                             creator=lambda tg: RelatedTags(tag=tg))

    def __repr__(self):
        return 'User(' + str(self.firstname) + ':' + str(self.id) + ')'

    def save_article(self, article):
        if article not in self.saved_articles:
            self.saved_articles.append(article)

    def un_save_article(self, article):
        if article in self.saved_articles:
            self.saved_articles.remove(article)

    def retrieve_articles(self):
        return self.saved_articles


# Automatically hashes the password passed into user while attempting to create one
@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value)
    return value


#  Given the news_article id, retrieve the users that are linked to it
#  print(NewsArticle.query.filter_by(id=4).first().users)
#  Retrieve all saved articles by the user, given the ID

class NewsArticle(db.Model):
    __tablename__ = 'newsarticle'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    link = db.Column(db.String(600), nullable=False)
    date_published = db.Column(db.DateTime, nullable=True)
    related_tags = db.relationship("Tag", secondary=related_tags,
                                   backref=db.backref('newsarticles'))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag = db.Column(db.String(100), nullable=False)

    users = association_proxy('user_list', 'user',
                              creator=lambda us: RelatedTags(user=us))

    def __init__(self, tag):
        self.tag = tag

    def __repr__(self):
        return 'Tag(' + str(self.tag) + ':' + str(self.id) + ')'


# MODELS THE M2M RELATIONSHIP BETWEEN USER AND TAG
# ROHAN ASOKAN ASKED FOR THIS
# EXAMPLE:
# User user views an article tagged 'entertainment' with object named tag
# This creates an relationship as so: [user <-- tag_count --> tag]
# Where the tag_count tracks the number of articles with tag 'tag' has been
# viewed by the user
# --------------
# 1) __init__ required when M2M is handled primarily in one direction (appending)
# 2) Get rid of __init__ via the 'creator' argument passed into `association_proxy(...)`
# 3) The parameter order in __init__ restricts bi-directionality
class RelatedTags(db.Model):
    __tablename__ = "relatedtags"
    tag_id = db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
    tag_count = db.Column('tag_count', db.Integer, default=1)

    user = db.relationship("User", backref=db.backref("user_tags"))
    # tag = db.relationship("Tag", backref=db.backref("user_list", cascade="all, delete-orphan"))
    tag = db.relationship("Tag", backref=db.backref("user_list"))

    # def __init__(self, tag=None, user=None, tag_count=0):
    #     print(user)
    #     self.user = user
    #     self.tag = tag
    #     self.tag_count = tag_count


    def __repr__(self):
        return 'relating ' + str(self.tag) + ' to ' + str(self.user)

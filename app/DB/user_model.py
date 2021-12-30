"""

    app 使用者資料庫模型

"""

from datetime import datetime


from app import db, login_manager
from .junction_table import user_collect_movies

class Users(db.Model):
    ''' 使用者資料庫模型 '''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(128), unique = True)
    username = db.Column(db.String(64), unique = True)
    password_hash = db.Column(db.String(128))
    avatar_hash = db.Column(db.String(32))
    member_since = db.Column(db.DateTime(), default = datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default = datetime.utcnow)

    collect_movies = db.relationship('Movies', secondary = user_collect_movies, backref = db.backref('users', lazy = 'dynamic'), lazy = 'dynamic')


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

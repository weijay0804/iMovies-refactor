"""

    資料庫關連表

"""

from app import db


user_collect_movies = db.Table(
    'user_collect_movies',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'))   
)

user_watched_movies = db.Table(
    'user_watched_movies',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id'))  
)


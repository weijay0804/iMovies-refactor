"""

    app 使用者資料庫模型

"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import hashlib


from app import db, login_manager
from .junction_table import user_collect_movies, user_watched_movies

class Users(db.Model, UserMixin):
    ''' 使用者資料庫模型 '''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(128), unique = True)
    username = db.Column(db.String(64), unique = True)
    password_hash = db.Column(db.String(128))
    avatar_hash = db.Column(db.String(32))
    member_since = db.Column(db.DateTime(), default = datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default = datetime.utcnow)

    collect_movies = db.relationship('Movies', secondary = user_collect_movies, backref = db.backref('collect_users', lazy = 'dynamic'), lazy = 'dynamic')
    watched_movies = db.relationship('Movies', secondary = user_watched_movies, backref = db.backref('watched_users', lazy = 'dynamic'), lazy = 'dynamic')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        if self.username is not None and self.avatar_hash is None:
            self.avatar_hash = self.gravatar_hash()


    @property
    def password(self) -> None:
        ''' 讓外部無法讀取 pssword 屬性 '''
        raise AttributeError('Password is not a readablb attribute.')

    @password.setter
    def password(self, password : str) -> None:
        ''' 將密碼雜湊後儲存至資料庫 '''

        self.password_hash = generate_password_hash(password)

    def verify_password(self, password : str) -> bool:
        ''' 檢查使用者密碼是否正確 '''

        return check_password_hash(self.password_hash, password)

    def ping(self) -> None:
        ''' 更新使用者登入時間 '''

        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()


    def gravatar_hash(self) -> str:
        ''' 根據使用者 username 產生 md5 hash 值'''

        hash = hashlib.md5(self.username.lower().encode('utf-8')).hexdigest()

        return hash

    def gravatar(self, size : int = 100, default : str = 'identicon', rating : str = 'g') -> str:
        ''' 生成使用者頭相 url '''

        url = 'https://www.gravatar.com/avatar'

        hash = self.avatar_hash or self.gravatar_hash()
        

        return f'{url}/{hash}?s={size}&d={default}&r={rating}'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

"""

    app 工廠函式

"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import  LoginManager, login_manager
from flask_moment import Moment

from docs.config import configs


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
moment = Moment()

# 指定 登入路由
login_manager.login_view = 'auth.login'

def create_app(config_name : str) -> Flask:
    ''' 建立 app '''

    # 產生 app 實例
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    configs[config_name].init_app(app)

    # 初使化 HTTPS 物件
    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    # 初使化套件
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    moment.init_app(app)

    # 註冊藍圖
    from .views.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .views.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app
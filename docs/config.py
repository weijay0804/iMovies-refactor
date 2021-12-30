"""

    app 設定檔

"""


import os
from dotenv import load_dotenv

# 初使化套件
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))    # 根目錄路徑

class Config():
    ''' app 基礎設定 '''

    TMDB_API_KRY = os.environ.get('TMDB_API_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 設為 False 能使用較少記憶體空間
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SSL_REDIRECT = False    # 要不要使用 HTTPS 協定


    @staticmethod
    def init_app(app):
        ''' 創建 app 實例 '''
        pass


class DevelopmentConfig(Config):
    ''' app 開發階段設定 '''

    DEBUG = True

    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_USER = os.environ.get('DB_USER')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')

    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'  # 使用 MySQL

class TestingConfig(Config):
    ''' app 測試階段設定 '''

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'   # 使用記憶體

class ProductionConfig(Config):
    ''' app 部屬階段設定 '''

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class HerokuConfig(ProductionConfig):
    ''' heroku 部屬設定 '''

    if os.environ.get('DATABASE_URL'):
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace('postgres', 'postgresql')  # 使用 PostgreSQL
    SSL_REDIRECT = True if os.environ.get('DYNO') else False    # 使用 HTTPS

    @classmethod
    def init_app(app):
        ProductionConfig.init_app(app)

        # 使用反向代理伺服器
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

configs = {
    'development' : DevelopmentConfig,
    'testing' : TestingConfig, 
    'production' : ProductionConfig,
    'heroku' : HerokuConfig,
}
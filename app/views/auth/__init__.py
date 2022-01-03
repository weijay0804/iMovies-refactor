'''

    使用者認證相關功能藍圖

'''


from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import view
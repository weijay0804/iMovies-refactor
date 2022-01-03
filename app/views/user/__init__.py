'''

    使用者相關功能藍圖

'''

from flask import Blueprint

user = Blueprint('user', __name__)

from . import view
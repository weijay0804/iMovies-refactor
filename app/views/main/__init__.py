"""

    app 主視圖藍圖

"""

from flask import Blueprint

main = Blueprint('main', __name__)

from . import view, errors
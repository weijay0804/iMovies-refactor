"""

    app 錯誤處理路由

"""

from flask import render_template

from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html')

@main.app_errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html')
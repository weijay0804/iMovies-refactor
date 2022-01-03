'''

    使用者相關路由

'''



from flask import request, flash, render_template, redirect, url_for

from app.DB.user_model import Users
from app import db

from . import auth

@auth.route('/login')
def login():
    return 'Login'

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    ''' 使用者註冊路由 '''

    # 處理表單
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 如果 email 存在資料庫，就發出錯誤訊息
        if Users.query.filter_by(email = email).first():
            flash('Email 已經被使用')
            return render_template('auth/register.html', email = email, username = username)

        # 如果 username 存在資料庫，就發出錯誤訊息
        if Users.query.filter_by(username = username).first():
            flash('使用者名稱已存在')
            return render_template('auth/register.html', email = email)

        # 如果密碼不相同，就發出錯誤訊息
        if password1 != password2:
            flash('密碼必須相同')
            return render_template('auth/register.html', email = email, username = username)

        u = Users(email = email, username = username, password = password1)
        db.session.add(u)
        db.session.commit()
        flash('註冊成功')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')
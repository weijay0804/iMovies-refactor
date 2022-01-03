'''

    使用者認證相關路由

'''



from flask import request, flash, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from app.DB.user_model import Users
from app import db

from . import auth


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

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    ''' 使用者登入路由 '''

    # 處理表單
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        u = Users.query.filter_by(email = email).first()

        if not u or not u.verify_password(password):
            flash('帳號或密碼錯誤')

            return redirect(url_for('auth.login'))
        login_user(u)
        return redirect(url_for('main.index'))


    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    ''' 使用者登出路由 '''
    
    # 更新使用者登入時間
    current_user.ping()
    logout_user()
    flash('你已經登出')
    return redirect(url_for('main.index'))
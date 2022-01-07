'''

    使用者相關功能路由

'''


from flask_login import current_user, login_required
from flask import render_template, abort, request, flash, redirect, url_for
from datetime import datetime

from . import user
from app import db
from app.DB.user_model import Users
from app.DB.movie_model import Movies
from app.DB.movie_model import MovieGenres
from app.DB.mongo import Mongo
from app.functions import movie_function


@user.route('/<id>/profile')
@login_required
def user_profile(id):
    ''' 使用者個人資料路由 '''

    # 取使用者
    user = Users.query.get_or_404(id)

    # 連線 mongoDB
    mongo = Mongo()
    mongo_db = mongo.client.imovies
    user_collection = mongo_db.user_info
    
    # 尋找使用者資料
    user_info = user_collection.find_one({'_id' : user.id})

    user_profile_datas = {}

    # 如果 mongoDB 裡面有找到資料
    if user_info:
        user_profile_datas = user_info['info']

    template_datas = {
        'user' : user,
        'user_profile_datas' : user_profile_datas,
        'now' : datetime.utcnow()
    }

    return render_template('user/user_profile.html', **template_datas)

@user.route('/<id>/profile/edit', methods = ['GET', 'POST'])
@login_required
def user_profile_edit(id):
    ''' 使用者編輯個人資料路由 '''

    # 取得使用者和電影類別清單
    user  = Users.query.get_or_404(id)
    genres_dict = MovieGenres.movie_genres_en

    # 使用者權限不足
    if current_user != user:
        abort(403)

    # 連線到 mongoDB
    mongo = Mongo()
    mongo_db = mongo.client.imovies
    user_info_collection = mongo_db.user_info

    # 尋找使用者資料
    user_info = user_info_collection.find_one({'_id' : user.id})

    user_profile_datas = {}

    # 如果有找到資料
    if user_info:
        user_profile_datas = user_info['info']

    # 如果有使用者的資料就拿取，如果沒有就儲存成 '' 
    template_datas = {
        'genres_dict' : genres_dict,
        'name' : user_profile_datas.get('name') if user_profile_datas.get('name') else '',
        'location' : user_profile_datas.get('location') if user_profile_datas.get('location') else '',
        'about_me' : user_profile_datas.get('about_me') if user_profile_datas.get('about_me') else '',
        'user_genres' : user_profile_datas.get('genres') if user_profile_datas.get('genres') else [] 
    }
    
    # 處理表單
    if request.method == 'POST':
        # 取得表單的資料
        name = request.form.get('name')
        location = request.form.get('location')
        about_me = request.form.get('about_me')
        movie_genres = []

        # 處理表單中的電影類別
        for genre in set(genres_dict.values()):
            if request.form.get(genre):
                movie_genres.append(request.form.get(genre))

        # 將更新後的資料轉成 document 格式
        datas = {
            '_id' : user.id,
            'info' : {
                'name' : name,
                'location' : location,
                'about_me' : about_me,
                'genres' : movie_genres
            }
        }

        # 如果 mongoDB 裡面已經存在使用者資料，就刪除
        if user_info:
            user_info_collection.delete_one({'_id' : user.id})
        
        # 新增使用者資料到 mongoDB
        user_info_collection.insert_one(datas)

        flash('更新完成')

        return redirect(url_for('user.user_profile', id = user.id))

    return render_template('user/user_profile_edit.html', **template_datas)

    
@user.route('<int:user_id>/collect_movies/add/<int:movie_id>')
@login_required
def user_add_collect_movie(user_id,movie_id):
    ''' 使用者新增電影到電影清單中路由 '''

    user = Users.query.get_or_404(user_id)
    movie = Movies.query.get_or_404(movie_id)

    if current_user != user:
        abort(403)

    user_collect_movies = user.collect_movies.all()

    if movie in user_collect_movies:
        flash('該電影已經在你的電影清單中')
        if request.referrer:
            return redirect(request.referrer)
        else:
            return redirect(url_for('main.index'))

    user.collect_movies.append(movie)
    db.session.commit()

    flash('新增成功')

    if request.referrer:
        return redirect(request.referrer)
    else:
        return  redirect(url_for('main.index'))

@user.route('/<int:user_id>/collect_movies/delete/<int:movie_id>')
@login_required
def user_delete_collect_movie(user_id, movie_id):
    ''' 使用者刪除收藏清單中的電影路由 '''

    user = Users.query.get_or_404(user_id)
    movie = Movies.query.get_or_404(movie_id)

    if current_user != user:
        abort(403)

    user_collect_movies = user.collect_movies.all()

    if movie in user_collect_movies:
        user.collect_movies.remove(movie)
        
        db.session.commit()
        flash('刪除成功')
    
        return redirect(url_for('user.user_collect_movies', user_id = user.id))

    return redirect(url_for('main.index'))


@user.route('<int:user_id>/collect_movies')
@login_required
def user_collect_movies(user_id):
    ''' 使用者收藏的電影清單路由 '''

    user = Users.query.get_or_404(user_id)

    if current_user != user:
        abort(403)
        
    page = request.args.get('page', 1, type=int)
    sort_type = request.args.get('sort')
    is_desc = request.args.get('desc')

    url_args = {'sort' : sort_type, 'desc' : is_desc, 'user_id' : user.id}

    movie_query = user.collect_movies
    movies_count = movie_query.count()

    if sort_type:
        query = movie_function.sort_movies(movie_query, sort_type, is_desc)
    else:
        query = movie_query

    pagination = query.paginate(page, per_page=10, error_out=False)

    movies = pagination.items

    template_datas = {
        'movies' : movies,
        'movies_count' : movies_count,
        'page' : page,
        'pagination' : pagination,
        'url_args' : url_args
    }
    return render_template('user/user_collect_movies.html', **template_datas)
    

    

    

    

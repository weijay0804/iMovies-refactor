"""

    app 主路由

"""


from flask_login import current_user
from flask import render_template, request, redirect
from sqlalchemy import or_
import random

from packages.crawler.model import TMDB


from . import main
from app.DB.movie_model import MovieGenres, Movies, Top250Movies, PopularMovies
from app.DB.mongo import Mongo
from packages.crawler import Main
from app.functions import movie_function


@main.app_context_processor
def inject_movie_genres():
    ''' 讓模板可以直接讀取電影類別 '''

    gneres = MovieGenres.movie_genres
    return dict(movie_genres = gneres)


@main.route('/')
def index():
    ''' 主頁面 '''

    # 隨機推薦的電影
    movie_row_count = int(Movies.query.count()) - 30
    movies = Movies.query.offset(int(movie_row_count * random.random())).limit(30)

    recommend_movies = []   # 推薦的電影
    recomend_genres = []    # 推薦的電影類別

    # 連接到 mongoDB
    mongo = Mongo()
    mongo_db = mongo.client.imovies
    user_info = mongo_db.user_info

    # 取得 user 資料
    # TODO 修改查詢內容
    user_data = user_info.find_one({'_id' : 1})
    user_like_genres = user_data['info'].get('genres')

    how_many_genres_want_to_show = 3

    # TODO 加上 current_user.is_authenticated
    # 如果使用者登入，並且使用者有勾選喜歡的類別
    if user_like_genres:
        # 如果使用者勾選的類別小於要顯示的數量，就直接全部拿出來
        if len(user_like_genres) <= how_many_genres_want_to_show:
            recomend_genres.extend(user_like_genres)
        
        # 如果類別數量大於，就隨機挑選
        else:
            random_genres = movie_function.get_user_recommend_movies(how_many_genres_want_to_show, user_like_genres)
            recomend_genres.extend(random_genres)

    # 如果使用者沒有登入，或是電影數量不夠，就再湊齊
    if len(recomend_genres) < how_many_genres_want_to_show:
        random_genres = movie_function.get_random_genres(how_many_genres_want_to_show - len(recomend_genres))
        recomend_genres.extend(random_genres)

    # 根據類別取出電影
    for genre in recomend_genres:
        rowCount = int(Movies.query.filter(Movies.genres.like(f'%{genre}%')).count()) - 10

        if rowCount <= 0:
            re_movies = Movies.query.filter(Movies.genres.like(f'%{genre}%')).all()
        else:
            re_movies = Movies.query.filter(Movies.genres.like(f'%{genre}%')).offset(int(rowCount * random.random())).limit(10).all()

        recommend_movies.append(list(re_movies))
    
    # 要傳入模板的資料
    template_datas = {
        'movies' : movies,
        'recommend_movies' : recommend_movies,
        'recommend_genres' : recomend_genres
    }

    return render_template('movies/index.html', **template_datas)

@main.route('/movies')
def movies():
    ''' 所有電影路由 '''

    page = request.args.get('page', 1, type=int)
    sort_type = request.args.get('sort')
    is_desc = request.args.get('desc')
    url_args = {'sort' : sort_type, 'desc' : is_desc}

    movie_query = Movies.query

    if sort_type:
        query = movie_function.sort_movies(movie_query, sort_type, is_desc)
    else:
        query = movie_query
    
    pagination = query.paginate(page, per_page=10, error_out=False)

    movies = pagination.items

    template_datas = {
        'movies' : movies,
        'pagination' : pagination,
        'page' : page,
        'url_args' : url_args
    }

    return render_template('movies/movies.html', **template_datas)


@main.route('/movies/top250')
def top250():
    ''' IMDb Top 250 電影路由 '''

    page = request.args.get('page', 1, type=int)
    sort_type = request.args.get('sort')
    is_desc = request.args.get('desc')
    url_args = {'sort' : sort_type, 'desc' : is_desc}

    movie_query = Movies.query.join(
        Top250Movies, Movies.tmdb_id == Top250Movies.tmdb_id
    )

    if sort_type:
        query = movie_function.sort_movies(movie_query, sort_type, is_desc)
    else:
        query = movie_query.order_by(Movies.rate.desc())
    
    pagination = query.paginate(page, per_page=10, error_out=False)

    movies = pagination.items

    template_datas = {
        'movies' : movies,
        'pagination' : pagination,
        'page' : page,
        'url_args' : url_args
    }

    return render_template('movies/top250.html', **template_datas)

@main.route('/movies/popular')
def popular_movies():
    ''' 熱門電影路由 '''

    page = request.args.get('page', 1, type = int)
    sort_type = request.args.get('sort')
    is_desc = request.args.get('desc')
    url_args = {'sort' : sort_type, 'desc' : is_desc}

    movie_query = Movies.query.join(
        PopularMovies, Movies.tmdb_id == PopularMovies.tmdb_id
    )

    if sort_type:
        query = movie_function.sort_movies(movie_query, sort_type, is_desc)
    else:
        query = movie_query
    
    pagination = query.paginate(page, per_page=10, error_out=False)

    movies = pagination.items

    template_datas = {
        'movies' : movies,
        'pagination' : pagination,
        'page' : page,
        'url_args' : url_args
    }

    return render_template('movies/popular.html', **template_datas)

# TODO　連接　MongoDB 拿資料
@main.route('/movies/<id>')
def movie(id):
    ''' 電影詳細頁面路由 '''

    # 初使化 TMDB API
    tmdb = Main().tmdb

    # 初使化 MongoDB 
    mongo = Mongo()
    mongo_db = mongo.client.imovies

    # movie detail collection
    movies_db = mongo_db.movie_detail
    # movie video collection
    movie_video = mongo_db.movie_video

    # 取得電影
    movie = Movies.query.get_or_404(id)

    # 取得電影詳細資料
    movie_detail = movies_db.find_one({'_id' : movie.tmdb_id})

    # 取得電影預告片資料
    movie_video = movie_video.find_one({'_id' : movie.tmdb_id})

    # 取得 netflix 連結
    netflix_link = tmdb.get_netflix_link(tmdb_id = movie.tmdb_id)

    similar_movies = []

    similar_movie_numbers = 8

    # 使用電影名稱尋找相似電影
    similar_movie_use_title = movie_function.use_movie_title_found_similar_movies(
        title = movie.title,
        original_title=movie.original_title,
        numbers=similar_movie_numbers
        )
    similar_movies.extend(similar_movie_use_title)

    # 如果相似電影數量不夠，就用電影類別尋找
    if (similar_movie_numbers - len(similar_movies)) != 0:
        movie_genre_list = movie.genres.split(',')
        movie_genre = movie_function.get_movie_genre_randomly(movie_genre_list, 1)[0]
        similar_movie_use_genre = Movies.query.filter(
            Movies.genres.like(f'%{movie_genre}%')
        ).limit(int(similar_movie_numbers - len(similar_movies))).all()
        similar_movies.extend(similar_movie_use_genre)

    template_datas = {
        'movie' : movie,
        'movie_detail' : movie_detail['datas'],
        'movie_video' : movie_video['video'],
        'comments' : [],
        'similar_movies' : similar_movies,
        'netxflix_link' : netflix_link
    }

    return render_template('movies/movie.html', **template_datas)

    

@main.route('/movies/search')
def movie_search():
    ''' 搜尋電影 路由 '''

    page = request.args.get('page', 1, type = int)
    sort_type = request.args.get('sort')
    is_desc = request.args.get('desc')
    search_key = request.args.get('key')

    url_args = {'sort' : sort_type, 'desc' : is_desc}

    # 如果搜尋框裡沒有資料，就導回前一頁
    if not search_key:
        return redirect(request.referrer)

    movie_query = Movies.query.filter(
        or_(
            (Movies.title.like(f'%{search_key}%')),
            (Movies.original_title.like(f'%{search_key}%'))
        )
    )

    if sort_type:
        query = movie_function.sort_movies(movie_query, sort_type, is_desc)
    else:
        query = movie_query
    
    pagination = query.paginate(page, per_page=10, error_out=False)

    movies = pagination.items

    template_datas = {
        'movies' : movies,
        'page' : page,
        'pagination' : pagination,
        'key' : search_key,
        'url_args' : url_args
    }

    return render_template('movies/search.html', **template_datas)


@main.route('/movies/genres/<genre>')
def movie_genre(genre):
    ''' 電影種類路由 '''

    page = request.args.get('page', 1, type = int)
    sort_type = request.args.get('sort')
    is_desc = request.args.get('desc')

    url_args = {'sort' : sort_type, 'desc' : is_desc, 'genre' : genre}

    movie_genre = genre

    movie_query = Movies.query.filter(
        Movies.genres.like(f'%{movie_genre}%')
    )

    if sort_type:
        query = movie_function.sort_movies(movie_query, sort_type, is_desc)
    else:
        query = movie_query
    
    pagination = query.paginate(page, per_page=10, error_out=False)

    movies = pagination.items
    print('----------------------')
    print('test')

    template_datas = {
        'movies' : movies,
        'page' : page,
        'pagination' : pagination,
        'genre' : movie_genre,
        'url_args' : url_args
    }

    return render_template('movies/movie_genre.html', **template_datas)


    
        
    






    



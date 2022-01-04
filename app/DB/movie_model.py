"""

    app 電影資料庫模型

"""


from datetime import datetime
import json
from app import db
from packages.decorators import execut_time




class MovieGenres():
    ''' 電影類型 '''

    movie_genres = [
        '冒險',
        '劇情',
        '動作',
        '科幻',
        '奇幻',
        '戰爭',
        '犯罪',
        '懸疑', 
        '驚悚',
        '恐怖',
        '西部',
        '歷史',
        '紀錄',
        '喜劇', 
        '家庭', 
        '動畫', 
        '電視電影', 
        '愛情', 
        '音樂',
    ]

    movie_genres_en = {
        '動作' : 'action',
        '犯罪' : 'crime',
        '戰爭' : 'war',
        '奇幻' : 'fantasy',
        '驚悚' : 'thriller',
        '動畫' : 'fantasy',
        '歷史' : 'history',
        '西部' : 'western',
        '冒險' : 'adventure',
        '科幻' : 'science-fiction',
        '恐怖' : 'crime',
        '電視電影' : 'TV-movie',
        '劇情' : 'drama',
        '懸疑' : 'mystery',
        '音樂' : 'music',
        '家庭' : 'family',
        '愛情' : 'romance',
        '喜劇' : 'comedy',
        '紀錄' : 'Documentary'
    }


class Movies(db.Model):
    ''' 電影資料庫模型 '''

    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key = True)
    tmdb_id = db.Column(db.Integer, unique = True, index = True)
    imdb_id = db.Column(db.String(15), unique = True)
    title = db.Column(db.Text)
    original_title = db.Column(db.Text)
    release_date = db.Column(db.Date)
    rate = db.Column(db.Float)
    poster_path = db.Column(db.String(40))
    genres = db.Column(db.Text)
    add_date = db.Column(db.Date)

    @staticmethod
    def __add_data(datas : dict) -> dict:
        ''' 加入資料到資料庫 '''

        movie_datas = datas['datas']

        movie = {
            'tmdb_id' : movie_datas['tmdb_id'],
            'imdb_id' : movie_datas['imdb_id'],
            'title' : movie_datas['title'],
            'original_title' : movie_datas['original_title'],
            'release_date' : datetime.strptime(movie_datas['release_date'], '%Y-%m-%d'),
            'rate' : movie_datas['vote_average'],
            'genres' : ','.join(movie_datas['genres']),
            'poster_path' : movie_datas['poster_path'],
            'add_date' : datetime.utcnow()
        }
           

        return movie

    
    @staticmethod
    @execut_time
    def insert(file_path : str):
        ''' 新增資料到 movies 資料庫 '''


        with open(file_path, 'r', encoding='utf-8') as f:
            datas = json.load(f)

        for data in datas:
            if not Movies.query.filter_by(tmdb_id = data['_id']).first():
                movie_datas = Movies.__add_data(data)
                movie = Movies(**movie_datas)
            else:
                continue

            db.session.add(movie)
        db.session.commit()

    @staticmethod
    @execut_time
    def update(file_path : str):
        ''' 更新資料庫中的資料 '''

        with open(file_path, 'r', encoding='utf-8') as f:
            datas = json.load(f)

        for data in datas:
            if Movies.query.filter_by(tmdb_id = data['_id']).first():
                updated_datas = Movies.__add_data(data)
                Movies.query.filter(Movies.tmdb_id == data['_id']).update(updated_datas)
            else:
                continue
        
        db.session.commit()


        

class PopularMovies(db.Model):
    ''' 熱門電影資料庫模型 '''

    __tablename__ = 'popularmovies'

    id = db.Column(db.Integer, primary_key = True)
    tmdb_id = db.Column(db.Integer, unique = True, index = True)
    add_date = db.Column(db.Date)


    @staticmethod
    def __add_data(datas : int):
        ''' 加入資料到 popularmovies 資料庫 '''

        movie = PopularMovies(
            tmdb_id = datas,
            add_date = datetime.utcnow()
        )

        return movie

    
    
    @staticmethod
    @execut_time
    def update(file_path : str):
        ''' 新增資料 '''

        PopularMovies.query.delete()

        with open(file_path, 'r', encoding='utf-8') as f:
            datas = json.load(f)

        for data in datas['result']:
            movie = PopularMovies.__add_data(datas = data)

            db.session.add(movie)

        db.session.commit()
            


class Top250Movies(db.Model):
    ''' IMDb TOP 250 電影資料庫模型 '''

    __tablename__ = 'top250movies'

    id = db.Column(db.Integer, primary_key = True)
    tmdb_id = db.Column(db.Integer, unique = True, index = True)
    add_date = db.Column(db.Date)

    @staticmethod
    def __add_data(datas : int):
        ''' 加入資料到 top250movies '''

        movie = Top250Movies(
            tmdb_id = datas,
            add_date = datetime.utcnow()
        )

        return movie


    @staticmethod
    @execut_time
    def update(file_path : str):
        ''' 新增資料 '''


        Top250Movies.query.delete()

        with open(file_path, 'r', encoding='utf-8') as f:
            datas = json.load(f)

        for data in datas['result']:
            movie = Top250Movies.__add_data(datas = data)

            db.session.add(movie)

        db.session.commit()




    

    
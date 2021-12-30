"""

    處理有關電影的函式

"""

from flask_sqlalchemy import BaseQuery
from sqlalchemy import or_

from app.DB.movie_model import MovieGenres, Movies
import random
import re


def get_random_genres(number_of_genre : int) -> list:
    ''' 從電影類別清單中隨機取特定數量的類別 '''
    
    genres = MovieGenres.movie_genres.copy()

    genres.remove('電視電影')
    genres.remove('紀錄')

    if len(genres) >= number_of_genre:
        result = []
        random_numbers = random.sample(range(0, len(genres)), number_of_genre)

        for number in random_numbers:
            result.append(genres[number])
    else:
        print('超出範圍')
        return None

    return result


def get_user_recommend_movies(numbers_of_genre : int, user_like_genres : list) -> list:
    ''' 從使用者喜歡的類別中，挑選特定數量的類別 '''

    # 移除電影類別，因為電影量太少
    if '電視電影' in user_like_genres:
        user_like_genres.remove('電視電影')
    
    if '紀錄' in user_like_genres:
        user_like_genres.remove('紀錄')

    # 檢查會不會超出 user genres 的範圍
    if numbers_of_genre > len(user_like_genres):
        print('超出範圍')
        return None

    result = []
    radnom_numbers = random.sample(range(0, len(user_like_genres)), numbers_of_genre)

    for number in radnom_numbers:
        result.append(user_like_genres[number])

    return result


def sort_movies(movie_query : BaseQuery ,sort_type : str, is_desc : bool) -> BaseQuery:
    ''' 排序電影 '''

    if sort_type == 'rate':
        if is_desc:
            query = movie_query.order_by(Movies.rate.desc())
        else:
            query = movie_query.order_by(Movies.rate)
    elif sort_type == 'year':
        if is_desc:
            query = movie_query.order_by(Movies.release_date.desc())
        else:
            query = movie_query.order_by(Movies.release_date)

    return query

def get_movie_genre_randomly(genre : list, number : int) -> list:
    ''' 從一部電影的類別中隨機選取類別 '''

    if len(genre) <= number:
        return genre

    result = []    
    random_numbers = random.sample(range(0, len(genre)), number)

    for number in random_numbers:
        result.append(genre[number])

    return result


def use_movie_title_found_similar_movies(title : str, original_title : str ,numbers : int) -> list:
    ''' 使用電影名稱尋找相同的電影 '''

    # 分割標題的正規表達示
    regex = re.compile(r'\D*')

    # 將電影名稱用 : 分割，再用數字分割 (蜘蛛人3:返校日 -> 蜘蛛人)
    movie_title = regex.findall(
        title.split('：')[0]
    ) [0]
    movie_original_title = regex.findall(
        original_title.split(':')[0]
    )[0]

    # 使用分割後的名稱尋找
    similar_movies = Movies.query.filter(
        or_(
            (Movies.title.like(f'%{movie_title}%')),
            (Movies.original_title.like(f'%{movie_original_title}%'))
        )
    ).limit(numbers).all()

    return similar_movies

def user_movie_genre_found_similar_movies(genre : str, number : int) -> list:
    ''' 使用電影類別隨機尋者相似的電影 '''

    rowCount = int(Movies.query.count()) - number

    similar_movies = Movies.query.filter(
        Movies.genres.like(f'%{genre}%')
    ).offset(int(rowCount * random.random())).limit(number).all()

    return similar_movies







    




    


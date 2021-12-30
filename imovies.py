"""

    app 主程式

"""

import os
import click
import time
from flask_migrate import Migrate
from app import create_app, db
from app.DB import movie_model, user_model
from app.DB.mongo import Mongo
from packages.crawler import Main


app = create_app(os.environ.get('FLASK_CONFIG') or 'development')

# 初使化 db 遷移腳本物件
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    ''' 讓物件能直接在 shell 使用 '''

    return dict(
        db = db,
        Movies = movie_model.Movies,
        Users = user_model.Users
    )

rootpath = os.path.abspath(os.path.dirname(__name__))
movie_datas_path = os.path.join(rootpath, 'movie_datas')


@app.cli.command()
@click.option('--type', '-t', 'type', help = 'type = top250 or popular', required = True)
def crawling(type):
    main = Main()

    if type == 'popular':
        popular_path = os.path.join(movie_datas_path, 'popular.json')
        popular_deatil_path = os.path.join(movie_datas_path, 'popular_detail.json')
        popular_video_path = os.path.join(movie_datas_path, 'popular_video.json')
        popular_cast_path = os.path.join(movie_datas_path, 'popular_cast.json')

        main.get_popular()
        time.sleep(0.5)
        main.get_movie_detail(input_file_path=popular_path, output_file_path=popular_deatil_path)
        main.get_movie_video(input_file_path=popular_path, output_file_path=popular_video_path)
        main.get_movie_cast(input_file_path=popular_path, output_file_path=popular_cast_path)

    if type == 'top250':
        top250_path = os.path.join(movie_datas_path, 'top250.json')
        top250_detail_path = os.path.join(movie_datas_path, 'top250_detail.json')
        top250_video_path = os.path.join(movie_datas_path, 'top250_video.json')
        top250_cast_path = os.path.join(movie_datas_path, 'top250_cast.json')

        main.get_top_250()
        time.sleep(0.5)
        main.get_movie_detail(input_file_path=top250_path, output_file_path=top250_detail_path)
        main.get_movie_video(input_file_path=top250_path, output_file_path=top250_video_path)
        main.get_movie_cast(input_file_path=top250_path, output_file_path=top250_cast_path)


@app.cli.command()
@click.option('--type', '-t', 'type', help = " which file you want to insert (top250, popular) ", required = True)
def mysqlinsert(type):

    if type == 'popular':
        file_path = os.path.join(movie_datas_path, 'popular_detail.json')
    elif type == 'top250':
        file_path = os.path.join(movie_datas_path, 'top250_detail.json')
    else:
        print(f'錯誤的指令 {type} ')
        return -1

    movie_model.Movies.insert(file_path=file_path)

    print('Done !')

@app.cli.command()
@click.option('--database', '-db', 'db', help = "which database you want to update (popular, top250, movies) ", required = True)
@click.option('--file', '-f', 'file', help = "what file you want to update to database (popular, top250) only when -db = movies needed ")
def mysqlupdate(db, file):

    if db == 'movies':
        if file == 'popular':
            file_path = os.path.join(movie_datas_path, 'popular_detail.json')
            movie_model.Movies.update(file_path=file_path)
        elif file == 'top250':
            file_path = os.path.join(movie_datas_path, 'top250_detail.json')
            movie_model.Movies.update(file_path=file_path)
        else:
            print(f'錯誤的指令 {db, file} ')
            return -1

    elif db == 'popular':
        file_path = os.path.join(movie_datas_path, 'popular.json')
        movie_model.PopularMovies.update(file_path=file_path)

    elif db == 'top250':
        file_path = os.path.join(movie_datas_path, 'top250.json')
        movie_model.Top250Movies.update(file_path=file_path)


@app.cli.command()
@click.option('--collcetion', '-c', 'collcetion', help = "which collection you want to insert (detail, video, cast) ", required = True)
@click.option('--file', '-f', help = "which file type (top250, popular) ", required = True)
def mongoinsert(collcetion, file):

    mongo = Mongo()
    db = mongo.client.imovies


    if collcetion == 'detail':
        db_collcetion = db.movie_detail
    elif collcetion == 'video':
        db_collcetion = db.movie_video
    elif collcetion == 'cast':
        db_collcetion = db.movie_cast
    else:
        print(f'錯誤的指令 {collcetion} ')
        return -1

    if file == 'popular':
        file_path = os.path.join(movie_datas_path, f'popular_{collcetion}.json')
    elif file == 'top250':
        file_path = os.path.join(movie_datas_path, f'top250_{collcetion}.json')
    else:
        print(f'錯誤的指令 {file} ')
        return -1

    mongo.insert(file_path=file_path, collection=db_collcetion)

@app.cli.command()
@click.option('--collcetion', '-c', 'collcetion', help = "which collection you want to insert (detail, video, cast) ", required = True)
@click.option('--file', '-f', help = "which file type (top250, popular) ", required = True)
def mongoupdate(collcetion, file):

    mongo = Mongo()
    db = mongo.client.imoives

    if collcetion == 'detail':
        db_collcetion = db.movie_detail
    elif collcetion == 'video':
        db_collcetion = db.movie_video
    elif collcetion == 'cast':
        db_collcetion = db.movie_cast
    else:
        print(f'錯誤的指令 {collcetion} ')
        return -1

    if file == 'popular':
        file_path = os.path.join(movie_datas_path, f'popular_{collcetion}.json')
    elif file == 'top250':
        file_path = os.path.join(movie_datas_path, f'top250_{collcetion}.json')
    else:
        print(f'錯誤的指令 {file} ')
        return -1

    mongo.update(file_path=file_path, collection=db_collcetion)




    

    

        

    
'''

    使用者相關功能路由

'''

from flask_login import current_user, login_required
from flask import render_template
from datetime import datetime

from . import user
from app.DB.user_model import Users
from app.DB.mongo import Mongo


@user.route('/<id>/profile')
@login_required
def user_profile(id):
    ''' 使用者個人資料路由 '''

    user = Users.query.get_or_404(id)

    mongo = Mongo()
    mongo_db = mongo.client.imovies
    user_collection = mongo_db.user_info
    user_info = user_collection.find_one({'_id' : user.id})

    user_profile_datas = {
        'name' : None,
        'location' : None,
        'about_me' : None,
        'favorite_movie_genres' : []
    }

    if user_info:
        user_profile_datas['name'] = user_info['info'].get('name')
        user_profile_datas['location'] = user_info['info'].get('location')
        user_profile_datas['about_me'] = user_info['info'].get('about_me')
        user_profile_datas['favorite_movie_genres'] = user_info['info'].get('genres')

    template_datas = {
        'user' : user,
        'user_profile_datas' : user_profile_datas,
        'now' : datetime.utcnow()
    }

    return render_template('user/user_profile.html', **template_datas)

    




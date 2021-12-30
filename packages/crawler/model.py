"""

    爬蟲模型

"""

import time
import os
import json
import requests
from bs4 import BeautifulSoup


movie_geners = {
            27 : '恐怖', 
            37 : '西部', 
            10402 : '音樂', 
            18 : '劇情', 
            10752 : '戰爭', 
            35 : '喜劇', 
            10749 : '愛情', 
            10770 : '電視電影', 
            53 : '驚悚', 
            36 : '歷史', 
            10751 : '家庭', 
            28 : '動作', 
            80 : '犯罪', 
            9648 : '懸疑', 
            12 : '冒險', 
            14 : '奇幻', 
            16 : '動畫', 
            878 : '科幻',
            99 : '紀錄',
        }

def send_request(url : str) -> requests:

        response = requests.get(url)

        if response.status_code != 200:
            print(f'連線錯誤 status code : {response.status_code}')
            return -1
        
        return response

class IMDb:
    """ IMDb 電影類別 """

    def __init__(self):

        self.base_url = 'https://www.imdb.com/'

    def crawl_top_250_movies(self, movie_limit : int = None) -> dict:
        """ 爬取 IMDb top 250 電影排名 """

        url = f'{self.base_url}chart/top/?ref_=nv_mv_250'
        response = send_request(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        movie_items = soup.find('tbody', class_ = 'lister-list').find_all('tr', limit = movie_limit)

        IMDB_top_250 = {}
        movies = []

        for movie_item in movie_items:
            imdb_id = movie_item.find('td', class_ = 'titleColumn').find('a').get('href').split('/')[2]
            movies.append(imdb_id)

        IMDB_top_250['result'] = movies

        return IMDB_top_250


class TMDB():
    """ TMDB API 類別 """

    def __init__(self, api_key : str):
        self.api_key = api_key
        self.base_url = 'https://api.themoviedb.org/3/'
        

    def use_imdb_id_get_tmdb_id(self, imdb_id : str) -> int:
        ''' 使用 IMDb ID 取得 TMDB ID '''

        url = f'{self.base_url}movie/{imdb_id}/external_ids?api_key={self.api_key}'

        response = send_request(url)

        result = json.loads(response.text)

        return result.get('id')

    def get_popular_movies(self) -> dict:
        ''' 取得 TMDB 熱門電影 '''

        result = {'result' : []}

        for page in range(1, 6):

            url = f'{self.base_url}movie/popular?api_key={self.api_key}&language=zh-TW&page={page}'

            response = send_request(url)

            datas = json.loads(response.text)
            
            for movie in datas['results']:

                result['result'].append(movie['id'])

        return result



    def get_movie_detail(self, tmdb_id : int) -> dict:
        ''' 取得電影詳細資料 '''

        url = f'{self.base_url}movie/{tmdb_id}?api_key={self.api_key}&language=zh-TW'

        response = send_request(url)

        movie_detail = json.loads(response.text)

        result = {}

        result['tmdb_id'] = movie_detail['id']
        result['imdb_id'] = movie_detail['imdb_id']
        result['title'] = movie_detail['title']
        result['original_title'] = movie_detail['original_title']
        result['original_language'] = movie_detail['original_language']
        result['vote_average'] = movie_detail['vote_average']
        result['budget'] = movie_detail['budget']
        result['release_date'] = movie_detail['release_date']
        result['runtime'] = movie_detail['runtime']
        result['status'] = movie_detail['status']
        result['backdrop_path'] = movie_detail['backdrop_path']
        result['poster_path'] = movie_detail['poster_path']
        result['genres'] = [movie_geners[genre['id']] for genre in movie_detail['genres']]
        result['overview'] = movie_detail['overview']

        return result

    def get_movie_videos(self, tmdb_id : int) -> list:
        ''' 取得電影的預告片 '''

        url = f'{self.base_url}movie/{tmdb_id}/videos?api_key={self.api_key}&language=zh-TW'

        response = send_request(url)

        datas = json.loads(response.text)

        if datas['results']:
            videos = datas['results']
        else:
            url = f'{self.base_url}movie/{tmdb_id}/videos?api_key={self.api_key}&language=en-US'
            response = send_request(url)
            datas = json.loads(response.text)
            videos = datas['results']
        
        result = []
        
        # 如果有資料
        for video in videos:
            # 影片平台必須是 youtube
            if video['site'] == 'YouTube':
                result.append(video['key'])  
            else: 
                continue
        
        return result

    def get_movie_cast(self, tmdb_id : int) -> dict:
        ''' 取得電影演員、導演等 '''

        url = f'{self.base_url}movie/{tmdb_id}/credits?api_key={self.api_key}&language=zh-TW'

        response = send_request(url)

        datas = json.loads(response.text)

        result = {'cast' : [], 'directing' : []}
        result['tmdb_id'] = datas['id']

        for cast in datas['cast']:
            temp1 = {
                'id' : cast['id'],
                'name' : cast['name'],
                'original_name' : cast['original_name'],
                'profile_path' : cast['profile_path']
            }

            result['cast'].append(temp1)

        for crew in datas['crew']:
            if crew['department'] == 'Directing' and crew['job'] == 'Director':
                temp2 = {
                    'id' : crew['id'],
                    'name' : crew['name'],
                    'original_name' : crew['original_name'],
                    'profile_paht' : crew['profile_path']
                }
            
                result['directing'].append(temp2)
            else:
                continue

        return result

    def get_netflix_link(self, tmdb_id : int) -> str:
        ''' 取得電影的 netflix 連結 '''

        url = f'{self.base_url}movie/{tmdb_id}/watch/providers?api_key={self.api_key}'

        response = send_request(url)

        datas = json.loads(response.text)

        netflix_link = ''

        if datas and datas.get('results').get('TW'):
            try:
                if datas['results'].get('TW').get('flatrate')[0].get('provider_name') == 'Netflix':
                    netflix_link = datas['results'].get('TW').get('link')
            except:
                pass
        
        return netflix_link

class Crawler:
    ''' 爬蟲類別 '''

    def __init__(self, api_key : str):

        self.imdb = IMDb()
        self.tmdb = TMDB(api_key=api_key)

    def crawl_imdb_top_250_movies(self, file_path : str, movie_items : int = None):
        ''' 爬取 imdb top 250 電影，並輸出 json 檔案 '''

        top250 = self.imdb.crawl_top_250_movies(movie_limit=movie_items)

        movies = {'result' : []}

        for imdb_id in top250['result']:
            tmdb_id = self.tmdb.use_imdb_id_get_tmdb_id(imdb_id=imdb_id)

            movies['result'].append(tmdb_id)
            print(tmdb_id)
            time.sleep(0.1)

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(movies, f, indent=4)

        print('Done !')

    def get_popular_movies(self, file_path : str):
        ''' 取得 TMDB 熱門電影，並輸出 json 檔 '''

        popular_movies = self.tmdb.get_popular_movies()

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(popular_movies, f, indent=4)

        print('Done !')

    def get_movie_detail(self, input_file_path : str, output_file_path : str):
        ''' 取得電影詳細資料，並輸出 json 檔 '''

        with open(input_file_path, 'r', encoding='utf-8') as f:
            movies = json.load(f)

        result = []

        for movie_id in movies['result']:
            movie_detail = self.tmdb.get_movie_detail(tmdb_id = movie_id)
            temp = {
                '_id' : movie_id,
                'datas' : movie_detail
            }
            result.append(temp)
            time.sleep(0.2)
            print(movie_detail)

        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4)

        print('Done !')

    def get_movie_videos(self, input_file_path : str, out_put_file_path : str):
        ''' 取得電影預告片，並輸出 json 檔 '''

        with open(input_file_path, 'r', encoding='utf-8') as f:
            movies = json.load(f)

        result = []

        for movie_id in movies['result']:
            video = self.tmdb.get_movie_videos(tmdb_id=movie_id)
            temp = {
                '_id' : movie_id,
                'video' : video
            }

            result.append(temp)
            time.sleep(0.1)
            print(temp)

        with open(out_put_file_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4)

        print('Done !')

    def get_movie_casts(self, input_file_path : str, output_file_path : str):
        ''' 取得電影的演員 導演，並輸出 json 檔 '''

        with open(input_file_path, 'r', encoding='utf-8') as f:
            movies = json.load(f)

        result = []

        for movie_id in movies['result']:
            casts = self.tmdb.get_movie_cast(tmdb_id=movie_id)

            temp = {
                '_id' : movie_id,
                'casts' : casts
            }

            result.append(temp)

            print(temp)
            time.sleep(0.1)

        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=4)

        print('Done !')






            










        









    

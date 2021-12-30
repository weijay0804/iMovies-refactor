"""

    爬蟲主程式

"""


from .model import Crawler, TMDB
from dotenv import load_dotenv
import os

class Main():

    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get('API_KEY')
        self.tmdb = TMDB(api_key=self.api_key)
        self.crawler = Crawler(api_key=self.api_key)
        self.rootdir = os.path.abspath(os.path.dirname(__name__))

    def get_top_250(self):
        ''' 取得 imdb top 250 '''

        file_path = os.path.join(self.rootdir, 'movie_datas', 'top250.json')

        self.crawler.crawl_imdb_top_250_movies(file_path=file_path)

    def get_popular(self):
        ''' 取得熱門電影 '''

        file_path = os.path.join(self.rootdir, 'movie_datas', 'popular.json')

        self.crawler.get_popular_movies(file_path=file_path)

    def get_movie_video(self, input_file_path : str, output_file_path : str):
        ''' 取得電影預告片 '''

        self.crawler.get_movie_videos(input_file_path=input_file_path, out_put_file_path=output_file_path)

    def get_movie_detail(self, input_file_path : str, output_file_path : str):
        ''' 取得電影詳細資料 '''

        self.crawler.get_movie_detail(input_file_path=input_file_path, output_file_path=output_file_path)

    def get_movie_cast(self, input_file_path : str, output_file_path : str):
        ''' 取得電影演員 '''

        self.crawler.get_movie_casts(input_file_path=input_file_path, output_file_path=output_file_path)


    






    











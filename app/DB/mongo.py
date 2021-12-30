'''

    操作 mongo DB

'''

from dotenv import load_dotenv
from pymongo import MongoClient
import json
import os
import certifi
from packages.decorators import execut_time

class Mongo:
    
    def __init__(self):
        load_dotenv()
        self.usernamne = os.environ.get('MONGO_USERNAME')
        self.password = os.environ.get('MONGO_PASSWORD')
        self.url = f'mongodb+srv://{self.usernamne}:{self.password}@cluster0.xvs25.mongodb.net/imovies?retryWrites=true&w=majority'
        self.client = MongoClient(self.url, tlsCAFile = certifi.where())
        

    @execut_time
    def insert(self, file_path : str, collection : MongoClient):
        ''' 新增資料到 collection '''

        with open(file_path, 'r', encoding='utf-8') as f:
            datas = json.load(f)

        for data in datas:

            key = {'_id' : data['_id']}
            search = collection.find_one(key)

            if not search:
                collection.insert_one(data)
            else:
                continue
        print('Done ! ')

    @execut_time
    def update(self, file_path : str, collection : MongoClient):
        ''' 更新 collection 的資料 '''

        with open(file_path, 'r', encoding='utf-8') as f:
            datas = json.load(f)

        for data in datas:

            key = {'_id' : data['_id']}
            search = collection.find_one(key)

            if search:
                collection.delete_one(key)
                collection.insert_one(key)
            else:
                continue
    
    def get(self, key : dict, collection : MongoClient) -> dict:
        ''' 取得資料 '''

        result = collection.find_one(key)

        if result:
            return result
        else:
            return {}
        
        

    
from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint
import json

#import os
# from dotenv import load_dotenv
#from urllib.parse import quote_plus # used to escape string

#load_dotenv()
DB_USER = 'caiomiglioli'
DB_PASSWORD = 'miglioli'
DB_CONNECT_URL = 'sistemas-distribuidos.pcp4inu.mongodb.net/?retryWrites=true&w=majority'

class MongoDBClient:
    def __init__(self):
        uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@{DB_CONNECT_URL}"
        self.client = MongoClient(uri)
        self.db = self.client['sample_mflix']
        self.collection = self.db['movies']
    
    def listByActor(self, actor):
        movies = self.collection.find({'cast': {'$regex': f'.*{actor}.*'}})
        return list(movies)
    
    def listByGenre(self, genre):
        movies = self.collection.find({'genres': {'$regex': f'.*{genre}.*'}})
        return list(movies)

    def delete(self, id):
        r = self.collection.delete_one({'_id': ObjectId(id)})
        return r.deleted_count
    
    def getByTitle(self, title):
        movie = self.collection.find_one({'title': {'$regex': f'.*{title}.*'}})
        return movie
    
    def create(self, movie):
        movie = json.loads(movie)
        movie.pop('id')
        id = self.collection.insert_one(movie)
        return id
#end db

if __name__ == "__main__":
    db = MongoDBClient()
    # x = db.getByGenre('Animation')
    # x = db.delete('573a1390f29313caabcd516c')
    x = db.getByTitle('Regeneration')
    pprint.pprint(x)
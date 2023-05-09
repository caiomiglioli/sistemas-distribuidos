from pymongo import MongoClient
import pprint

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

    def get_client(self):
        return self.db
    
    def getByActor(self, actor):
        movies = self.collection.find({'cast': {'$regex': f'.*{actor}.*'}})
        return list(movies)
    
    def getByGenre(self, genre):
        movies = self.collection.find({'genres': {'$regex': f'.*{genre}.*'}})
        return list(movies)
#end dbclient


if __name__ == "__main__":
    db = MongoDBClient()
    x = db.getByGenre('Animation')
    pprint.pprint(x)
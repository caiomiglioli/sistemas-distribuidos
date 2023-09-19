from pymongo import MongoClient
from bson.objectid import ObjectId
import pprint
import json

#import os
# from dotenv import load_dotenv
#from urllib.parse import quote_plus # used to escape string

#load_dotenv()
DB_USER = 'x'
DB_PASSWORD = 'x'
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
    
    def getById(self, id):
        return self.collection.find_one({'_id': ObjectId(id)})
    
    def create(self, movie):
        movie = json.loads(movie)
        if movie.get('id'):
            movie.pop('id')
        id = self.collection.insert_one(movie)
        return id
    
    def update(self, id, movie):
        movie = json.loads(movie)
        if movie.get('id'):
            movie.pop('id')
        result = self.collection.update_one({'_id': ObjectId(id)}, { "$set": movie })
        return result.modified_count
#end db

if __name__ == "__main__":
    db = MongoDBClient()
    # x = db.getByGenre('Animation')
    # x = db.delete('573a1390f29313caabcd516c')
    x = db.getByTitle('Regeneration')

    # mJson = {
    #     'plot': 'Teste de novo :D',
    #     'genres': ['Teste'],
    #     'runtime': 120,
    #     'rated': 'NOT RATED',
    #     'cast': ['Disney', 'Braia'],
    #     'poster': 'https://i.imgur.com/3wMqz44.jpeg',
    #     'title': 'Teste',
    #     'fullplot': "Disney e Braia tentam passar na materia do mano Camps.",
    #     'year': 2023,
    #     'type': 'movie',
    #     'writers': ['Disney', 'Braia'],
    #     'countries': ['BRA'],
    #     'languages': ['Portuguese'],
    #     'directors': ['Campiolo'],
    # }
    # x = db.update('573a1390f29313caabcd6377', mJson)
    pprint.pprint(x)
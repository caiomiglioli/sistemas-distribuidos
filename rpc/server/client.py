
import asyncio
import grpc
import movies_pb2
import movies_pb2_grpc
from db import MongoDBClient

async def ListByGenre(stub, genre):
    msg = movies_pb2.Msg(message = genre)
    movies = stub.ListByGenre(msg)
    async for movie in movies:
        print('=============================== movie')
        print(movie)

async def ListByActor(stub, actor):
    msg = movies_pb2.Msg(message = actor)
    movies = stub.ListByActor(msg)
    async for movie in movies:
        print('=============================== movie')
        print(movie)

async def Create(stub, movieDict):
    movie = movieToProtobuf(movieDict)
    result = await stub.Create(movie)
    print('=============================== Result')
    print(result.message)

async def Delete(stub, movieID):
    msg = movies_pb2.Msg(message = movieID)
    result = await stub.Delete(msg)
    print('=============================== Result')
    print(result.message)
    
async def Read(stub, title):
    msg = movies_pb2.Msg(message = title)
    movie = await stub.Read(msg)
    print('=============================== movie')
    print(movie)

def movieToProtobuf(movie):
    """
    Cria e retorna uma instância de protobuf Movie a
    partir de um dicionário (movie).
    """
    m = movies_pb2.Movie()
    if movie.get('_id'): m.id = str(movie['_id'])
    m.title = movie['title'] if movie.get('title') else "N/A"
    m.poster = movie['poster'] if movie.get('poster') else "N/A"
    m.rated = movie['rated'] if movie.get('rated') else "N/A"
    m.type = movie['type'] if movie.get('type') else "N/A"
    m.plot = movie['plot'] if movie.get('plot') else "N/A"
    m.fullplot = movie['fullplot'] if movie.get('fullplot') else "N/A"
    m.runtime = movie['runtime'] if movie.get('runtime') else -1
    m.year = int(str(movie.get('year')).split('è')[0]) if movie.get('year') else -1
    if movie.get('cast'): m.cast.extend(movie['cast'])
    if movie.get('genres'): m.genres.extend(movie['genres'])
    if movie.get('countries'): m.countries.extend(movie['countries'])
    if movie.get('directors'): m.directors.extend(movie['directors'])
    if movie.get('writers'): m.writers.extend(movie['writers'])
    if movie.get('languages'): m.writers.extend(movie['languages'])
    return m #.SerializeToString()


async def main():
    async with grpc.aio.insecure_channel('localhost:7777') as channel:
        stub = movies_pb2_grpc.MoviesStub(channel)

        # print("-------------- ListByGenre --------------")
        # await ListByGenre(stub, "Animation")
        
        # print("-------------- ListByActor --------------")
        # await ListByActor(stub, "James")
        
        # print("-------------- Delete --------------")
        # await Delete(stub, "645ad90f51be4e778f48395a")
        
        # print("-------------- Read --------------")
        # await Read(stub, "Ace")
        
        print("-------------- Create --------------")
        mJson = {
            'plot': 'Teste de novo :D',
            'genres': ['Teste'],
            'runtime': 120,
            'rated': 'NOT RATED',
            'cast': ['Disney', 'Braia'],
            'poster': 'https://i.imgur.com/3wMqz44.jpeg',
            'title': 'Teste',
            'fullplot': "Disney e Braia tentam passar na materia do mano Camps.",
            'year': 2023,
            'type': 'movie',
            'writers': ['Disney', 'Braia'],
            'countries': ['BRA'],
            'languages': ['Portuguese'],
            'directors': ['Campiolo'],
        }
        await Create(stub, mJson)
#end main

if __name__ == '__main__':
    asyncio.run(main())
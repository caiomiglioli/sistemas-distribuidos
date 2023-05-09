import threading
import socket
import os

import movies_pb2
from db import MongoDBClient
from google.protobuf.json_format import MessageToJson

import datetime

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    db = MongoDBClient()

    try:
        server.bind(('localhost', 7777))
        server.listen()
    except:
        server.close()
        return print ("Desligando servidor")

    # Para cada nova conexão, é gerado uma thread que executa a função
    # 'orchestra', que por sua vez, aguarda os comandos do cliente.
    while True:
        client, ip = server.accept()
        thread = threading.Thread(target=orchestra, args=[client, ip, db])
        thread.start()
#end main

def orchestra(client, ip, db):
    """
    Função responsável por orquestrar os comandos recebidos do cliente,
    chamando as funções corretas baseadas no código do comando recebido
    no pacote do cliente.

    Esta função é executada em uma thread separada para cada usuário conectado.
    Recebe um socket 'Client' como argumento.
    """

    print('cliente conectado')
    
    while True:
        try:
            cmdSize = int.from_bytes(client.recv(4), 'big', signed=False)
            data = client.recv(cmdSize)
            
            if not data: 
                break
            
            cmd = movies_pb2.Command()
            cmd.ParseFromString(data)
            print(f'REQ: {ip} > {cmd.cmd} with {cmd.args}')

            match cmd.cmd:
                case "ListByGenre":
                    res = handleListByGenre(db, cmd.args[0])
                
                case "ListByActor":
                    res = handleListByActor(db, cmd.args[0])

                case "Create":
                    res = handleCreate(client, db)

                case "Retrieve":
                    res = handleRetrieve(db, cmd.args[0])

                case "Delete":
                    res = handleDelete(db, cmd.args[0])
            #end switchcase
            sendResponse(client, res)

        except Exception as e:
            print(e)
            print("cannot receive data")
            break

    print('cliente perdeu a conexão')
    client.close()
#end orchestra

# =====================================================

def handleListByGenre(db, genre):
    movies = db.listByGenre(genre)
    moviesList = movies_pb2.MoviesList()
    for movie in movies:
        moviesList.movies.append(movieToProtobuf(movie))
    return moviesList.SerializeToString()
#end getbygenre

def handleListByActor(db, actor):
    movies = db.listByActor(actor)
    moviesList = movies_pb2.MoviesList()
    for movie in movies:
        moviesList.movies.append(movieToProtobuf(movie))
    return moviesList.SerializeToString()
#end getbygenre

def handleDelete(db, movieId):
    result = db.delete(movieId)
    cmd = movies_pb2.Command()
    cmd.cmd = 'Success' if result else 'Failure'
    return cmd.SerializeToString()
#end delete

def handleRetrieve(db, name):
    movie = db.getByTitle(name)
    if movie:
        return movieToProtobuf(movie).SerializeToString()
    return movieToProtobuf({'_id': 'Nao encontrado'}).SerializeToString()
#end retrieve

def handleCreate(client, db):
    reqSize = int.from_bytes(client.recv(4), 'big', signed=False)
    req = client.recv(reqSize)
    m = movies_pb2.Movie()
    m.ParseFromString(req)

    result = db.create(MessageToJson(m))
    cmd = movies_pb2.Command()
    cmd.cmd = 'Success' if result else 'Failure'
    return cmd.SerializeToString()

# =====================================================

def sendResponse(client, msg):
    print(len(msg))
    size = len(msg).to_bytes(4, 'big', signed=False)
    client.send(size)
    client.send(msg)
#end sendResponde

def movieToProtobuf(movie):
    m = movies_pb2.Movie()
    m.id = str(movie['_id'])
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

# =====================================================
if __name__ == "__main__":
    main()

    # m = {
    #     '_id': '573a1392f29313caabcda6f1',
    #     'plot': 'Mickey and his band are determined to perform their music despite the interferance of Donald Duck and a powerful storm.',
    #     'genres': ['Family', 'Comedy', 'Animation'],
    #     'runtime': 9,
    #     'cast': ['Clarence Nash'],
    #     'title': 'The Band Concert',
    #     'fullplot': "Mickey is trying to lead a concert of The William Tell Overture, but he's continually disrupted by ice cream vendor Donald, who uses a seemingly endless supply of flutes to play Turkey in the Straw instead. After Donald gives up, a bee comes along and causes his own havoc. The band then reaches the Storm sequence, and the weather also starts to pick up; a tornado comes along, but they keep playing.",
    #     'languages': ['English'],
    #     'released': datetime.datetime(1935, 2, 23, 0, 0),
    #     'directors': ['Wilfred Jackson'],
    #     'awards': {'wins': 1, 'nominations': 0, 'text': '1 win.'},
    #     'lastupdated': '2015-08-05 00:51:48.930000000',
    #     'year': 1935,
    #     'imdb': {'rating': 7.9, 'votes': 1645, 'id': 26094},
    #     'countries': ['USA'], 'type': 'movie',
    #     'tomatoes': {'viewer': {'rating': 3.5, 'numReviews': 71, 'meter': 78},
    #     'dvd': datetime.datetime(2003, 3, 25, 0, 0),
    #     'production': 'Orbis Film',
    #     'lastUpdated': datetime.datetime(2015, 8, 22, 19, 5, 21)},
    #     'num_mflix_comments': 0
    # }
    # print(movieToProtobuf(m))
"""
Este código implementa a parte servidor de um programa cliente/servidor
de gerenciamento de uma base de dados de filmes, onde a comunicação
ocorre sockets TCP e formato Protobuf para cominucação.

Autores:
  - Caio Miglioli @caiomiglioli
  - Ryan Lazaretti @ryanramos01

Data de Criação: 06 de Abril de 2023
Ultima alteração: 09 de Abril de 2023
"""


import threading
import socket
import os

import movies_pb2
from db import MongoDBClient
from google.protobuf.json_format import MessageToJson

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    db = MongoDBClient() #conecta com o banco de dados

    try:
        server.bind(('localhost', 7778))
        server.listen()

        # Para cada nova conexão, é gerado uma thread que executa a função
        # 'orchestra', que por sua vez, aguarda os comandos do cliente.
        while True:
            client, ip = server.accept()
            thread = threading.Thread(target=orchestra, args=[client, ip, db])
            thread.start()

    except:
        server.close()
        return print ("Desligando servidor")
#end main

def orchestra(client, ip, db):
    """
    Função responsável por orquestrar os comandos recebidos do cliente,
    chamando as funções corretas baseadas no comando recebido no pacote do cliente.

    Esta função é executada em uma thread separada para cada usuário conectado.
    Recebe um socket 'Client' e o ip como argumento, e também uma instância do conector
    do MongoDB "db" (MongoDBClient).
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

                case "Update":
                    res = handleUpdate(client, db, cmd.args[0])

                case "Read":
                    res = handleRead(db, cmd.args[0])

                case "Delete":
                    res = handleDelete(db, cmd.args[0])
            #end switchcase
            sendResponse(client, res)

        except Exception as e:
            print(e)
            break

    print('cliente desconectado')
    client.close()
#end orchestra

# =====================================================

def handleListByGenre(db, genre):
    """
    Busca os filmes no banco de dados com o filtro Genre
    converte em protobuf e retorna tudo serializado para
    que se possa enviar para o cliente
    """
    movies = db.listByGenre(genre)
    moviesList = movies_pb2.MoviesList()
    for movie in movies:
        moviesList.movies.append(movieToProtobuf(movie))
    return moviesList.SerializeToString()
#end getbygenre

def handleListByActor(db, actor):
    """
    Busca os filmes no banco de dados com o filtro Actor
    converte em protobuf e retorna tudo serializado para
    que se possa enviar para o cliente
    """
    movies = db.listByActor(actor)
    moviesList = movies_pb2.MoviesList()
    for movie in movies:
        moviesList.movies.append(movieToProtobuf(movie))
    return moviesList.SerializeToString()
#end getbygenre

def handleDelete(db, movieId):
    """
    Deleta o filme do banco de dados através de o ID e
    retorna em protobuf o resultado (se teve sucesso ou
    falha)
    """
    result = db.delete(movieId)
    cmd = movies_pb2.Command()
    cmd.cmd = 'Success' if result else 'Failure'
    return cmd.SerializeToString()
#end delete

def handleRead(db, name):
    """
    Busca um filme no banco de dados com o filtro Title
    converte em protobuf e retorna tudo serializado para
    que se possa enviar para o cliente.
    """
    movie = db.getByTitle(name)
    if movie:
        return movieToProtobuf(movie).SerializeToString()
    return movieToProtobuf({'_id': 'Nao encontrado'}).SerializeToString()
#end retrieve

def handleCreate(client, db):
    """
    Recebe um protobuf do tipo movie do cliente, transforma
    em Json e envia pro banco de dados criar a instância.
    Retorna um protobuf serializado com o resultado da operação
    """
    reqSize = int.from_bytes(client.recv(4), 'big', signed=False)
    req = client.recv(reqSize)
    m = movies_pb2.Movie()
    m.ParseFromString(req)

    result = db.create(MessageToJson(m))
    cmd = movies_pb2.Command()
    cmd.cmd = 'Success' if result else 'Failure'
    return cmd.SerializeToString()
#end create

def handleUpdate(client, db, movieId):
    """
    Busca um filme no banco de dados com o filtro ID
    converte em protobuf e retorna tudo serializado para
    o cliente. Após isso, recebe um protobuf do tipo movie
    do cliente, transforma em Json e envia pro banco de dados
    editar a instância.
    Retorna um protobuf serializado com o resultado da operação
    """
    #envio os dados do filme
    m = db.getById(movieId)
    if not m:
        return movieToProtobuf({'_id': 'Nao encontrado'}).SerializeToString()
    movie = movieToProtobuf(m).SerializeToString()
    sendResponse(client, movie)

    #recebe os dados atualizados e atualiza no banco
    reqSize = int.from_bytes(client.recv(4), 'big', signed=False)
    req = client.recv(reqSize)
    m = movies_pb2.Movie()
    m.ParseFromString(req)
    result = db.update(movieId, MessageToJson(m))

    #retorna status
    cmd = movies_pb2.Command()
    cmd.cmd = 'Success' if result else 'Failure'
    return cmd.SerializeToString()
#end update

# =====================================================

def sendResponse(client, msg):
    """
    Envia pacotes do servidor ao cliente na seguinte ordem:
    Tamanho do pacote (4bytes)
    Pacote (Tamanho do Pacote bytes)
    Pacote pode ser diferentes tipos de protobuf
    """
    print(len(msg))
    size = len(msg).to_bytes(4, 'big', signed=False)
    client.send(size)
    client.send(msg)
#end sendResponde

def movieToProtobuf(movie):
    """
    Cria e retorna uma instância de protobuf Movie a
    partir de um dicionário (movie).
    """
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
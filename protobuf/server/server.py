import threading
import socket
import os

import movies_pb2
from db import MongoDBClient

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    db = MongoDBClient()

    try:
        server.bind(('localhost', 7778))
        server.listen()
    except:
        return print('\nErro ao iniciar o servidor.')

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
                case "GetByGenre":
                    res = handleGetByGenre(db, cmd.args[0])
                    sendResponse(client, res)

        except Exception as e:
            print(e)
            print("cannot receive data")
            break

    print('cliente perdeu a conexão')
    client.close()
#end orchestra

# =====================================================

def handleGetByGenre(db, genre):
    movies = db.getByGenre(genre)

    ml = list()
    for movie in movies:
        ml.append(movieToProtobuf(movie))

    moviesList = movies_pb2.MoviesList()
    moviesList.movies.extend(ml)
    return moviesList.SerializeToString()
#end getbygenre

# =====================================================

def sendResponse(client, msg):
    size = len(msg).to_bytes(4, 'big', signed=False)
    client.send(size)
    client.send(msg)
#end sendResponde

def movieToProtobuf(movie):
    print(movie)
    m = movies_pb2.Movie()
    m.id = str(movie['_id'])
    m.plot = movie['plot'] if movie['plot'] else "N/A"
    m.genres.extend(movie['genres'])
    m.runtime = movie['runtime'] if movie['runtime'] else "N/A"


    print("antes do rated, ", print(movie['rated']))

    if movie['rated']:
        m.rated = movie['rated']
    
    print("passou do rated")

    m.cast.extend(movie['cast'])
    m.poster = movie['poster'] if movie['poster'] else "N/A"
    m.title = movie['title'] if movie['title'] else "N/A"
    m.fullplot = movie['fullplot'] if movie['fullplot'] else "N/A"
    m.countries.extend(movie['countries'])
    m.directors.extend(movie['directors'])
    m.writers.extend(movie['writers'])
    m.year = movie['year'] if movie['year'] else "N/A"
    return m #.SerializeToString()

# =====================================================
if __name__ == "__main__":
    main()
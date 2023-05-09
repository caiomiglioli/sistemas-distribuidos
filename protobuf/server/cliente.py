import socket
import movies_pb2
import datetime

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 7777))
    print('Conectado.')
    
    # # --------------------------------------------------------------------

    # #enviar requisição "ListByGenre" com os argumentos "Animation"
    # cmd = movies_pb2.Command()
    # cmd.cmd = "ListByGenre"
    # cmd.args.append("History")

    # msg = cmd.SerializeToString()
    # size = len(msg).to_bytes(4, 'big', signed=False)
    # client.send(size)
    # client.send(msg)

    # #receber resposta do ListByGenre
    # resSize = int.from_bytes(client.recv(4), 'big', signed=False)
    
    # res = b''
    # while len(res) < resSize:
    #     res = res + client.recv(resSize)

    # moviesList = movies_pb2.MoviesList()
    # moviesList.ParseFromString(res)
    
    # # print(moviesList)
    # for m in moviesList.movies:
    #     print(m)

    # # --------------------------------------------------------------------

    # #enviar requisição "ListByActor" com os argumentos "Stanley Hunt"
    # cmd = movies_pb2.Command()
    # cmd.cmd = "ListByActor"
    # cmd.args.append("Stanley")

    # msg = cmd.SerializeToString()
    # size = len(msg).to_bytes(4, 'big', signed=False)
    # client.send(size)
    # client.send(msg)

    # #receber resposta do ListByActor
    # resSize = int.from_bytes(client.recv(4), 'big', signed=False)
    
    # res = b''
    # while len(res) < resSize:
    #     res = res + client.recv(resSize)

    # moviesList = movies_pb2.MoviesList()
    # moviesList.ParseFromString(res)
    
    # # print(moviesList)
    # for m in moviesList.movies:
    #     print(m)

    # # --------------------------------------------------------------------

    # #enviar requisição "Delete" com os argumentos "573a1390f29313caabcd5293"
    # cmd = movies_pb2.Command()
    # cmd.cmd = "Delete"
    # cmd.args.append("573a1390f29313caabcd5293")

    # msg = cmd.SerializeToString()
    # size = len(msg).to_bytes(4, 'big', signed=False)
    # client.send(size)
    # client.send(msg)

    # #receber resposta com o status do Delete
    # resSize = int.from_bytes(client.recv(4), 'big', signed=False)
    # res = client.recv(resSize)

    # cmd = movies_pb2.Command()
    # cmd.ParseFromString(res)

    # if cmd.cmd == 'Success':
    #     print('Instância removida com sucesso.')
    # else:
    #     print('Instância não removida.')

    # # --------------------------------------------------------------------

    # #enviar requisição "Retrieve" (getByTitle) com os argumentos "Regeneration"
    # cmd = movies_pb2.Command()
    # cmd.cmd = "Retrieve"
    # cmd.args.append("Regeneration")

    # msg = cmd.SerializeToString()
    # size = len(msg).to_bytes(4, 'big', signed=False)
    # client.send(size)
    # client.send(msg)

    # # #receber resposta com o filme encontrado
    # resSize = int.from_bytes(client.recv(4), 'big', signed=False)
    # res = client.recv(resSize)
    # movie = movies_pb2.Movie()
    # movie.ParseFromString(res)
    # print(movie)

    # # --------------------------------------------------------------------

    #enviar requisição "Create" sem argumentos
    cmd = movies_pb2.Command()
    cmd.cmd = "Create"
    # cmd.args.append("Regeneration")

    msg = cmd.SerializeToString()
    size = len(msg).to_bytes(4, 'big', signed=False)
    client.send(size)
    client.send(msg)

    # #Enviar dados do filme
    movie = movieToProtobuf({
        '_id': 'NEW',
        'plot': 'Teste',
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
    })

    msg = movie.SerializeToString()
    size = len(msg).to_bytes(4, 'big', signed=False)
    client.send(size)
    client.send(msg)

    #receber resposta com o status do Create
    resSize = int.from_bytes(client.recv(4), 'big', signed=False)
    res = client.recv(resSize)

    cmd = movies_pb2.Command()
    cmd.ParseFromString(res)

    if cmd.cmd == 'Success':
        print('Instância adicionada com sucesso.')
    else:
        print('Instância não adicionada.')

    # # --------------------------------------------------------------------

    print("fim.")
    client.close()
#end main

# Create > pokas de qualquer maneira
# Retrieve > nome do filme
# Update > id
# Delete > id

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
    if movie.get('languages'): m.languages.extend(movie['languages'])
    return m #.SerializeToString()

# =======
main()
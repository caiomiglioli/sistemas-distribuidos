import socket
import movies_pb2

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 7778))
    print('Conectado.')
    
    #enviar requisição "GetByGenre" com os argumentos "Animation"
    cmd = movies_pb2.Command()
    cmd.cmd = "GetByGenre"
    cmd.args.extend(["Animation"])

    msg = cmd.SerializeToString()
    size = len(msg).to_bytes(4, 'big', signed=False)

    client.send(size)
    client.send(msg)
    print("Comando enviado")

    #receber resposta do GetByGenre
    resSize = int.from_bytes(client.recv(4), 'big', signed=False)
    data = client.recv(resSize)
    print("Resposta recebida...")
    print(data)

    moviesList = movies_pb2.MoviesList()
    moviesList.ParseFromString(data)

    for m in moviesList.movies:
        m = movies_pb2.Movie()
        m.ParseFromString(data)
        print(m)
    print("Resposta processada.")

    client.close()
#end main

# =======
main()
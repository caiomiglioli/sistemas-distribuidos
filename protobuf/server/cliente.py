import socket
import movies_pb2
import datetime

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 7778))
    print('Conectado.')
    

    # # --------------------------------------------------------------------
    # #enviar requisição "GetByGenre" com os argumentos "Animation"
    # cmd = movies_pb2.Command()
    # cmd.cmd = "GetByGenre"
    # cmd.args.append("History")

    # msg = cmd.SerializeToString()
    # size = len(msg).to_bytes(4, 'big', signed=False)

    # client.send(size)
    # client.send(msg)

    # #receber resposta do GetByGenre
    # resSize = int.from_bytes(client.recv(4), 'big', signed=False)
    
    # res = b''
    # while len(res) < resSize:
    #     res = res + client.recv(resSize)

    # moviesList = movies_pb2.MoviesList()
    # moviesList.ParseFromString(res)
    
    # # print(moviesList)
    # for m in moviesList.movies:
    #     print(m)
    # print("fim.")
    # # --------------------------------------------------------------------

    # #enviar requisição "GetByActor" com os argumentos "Stanley Hunt"
    # cmd = movies_pb2.Command()
    # cmd.cmd = "GetByActor"
    # cmd.args.append("Stanley")

    # msg = cmd.SerializeToString()
    # size = len(msg).to_bytes(4, 'big', signed=False)

    # client.send(size)
    # client.send(msg)

    # #receber resposta do GetByActor
    # resSize = int.from_bytes(client.recv(4), 'big', signed=False)
    
    # res = b''
    # while len(res) < resSize:
    #     res = res + client.recv(resSize)

    # moviesList = movies_pb2.MoviesList()
    # moviesList.ParseFromString(res)
    
    # # print(moviesList)
    # for m in moviesList.movies:
    #     print(m)
    # print("fim.")

    # --------------------------------------------------------------------

    client.close()
#end main

# =======
main()
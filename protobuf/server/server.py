import threading
import socket
import os

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind(('localhost', 7777))
        server.listen()
    except:
        return print('\nErro ao iniciar o servidor.')

    # Para cada nova conexão, é gerado uma thread que executa a função
    # 'orchestra', que por sua vez, aguarda os comandos do cliente.
    while True:
        client, ip = server.accept()
        thread = threading.Thread(target=orchestra, args=[client])
        thread.start()
#end main

def orchestra(client):
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
            data = client.recv(2048).decode('utf-8')           
            print(data)
            # match cmdId:
            #     #connect
            #     case 0:
            #         sessionUser = handleLogin(client, frame)

        except Exception as e:
            print(e)
            print("cannot receive data")
            break

        if not data: 
            break

    print('cliente perdeu a conexão')
    client.close()
#end orchestra
import threading
import socket

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        server.bind(('localhost', 7777))
        server.listen()
    except:
        return print('\nErro ao iniciar o servidor.')

    while True:
        client, ip = server.accept()
        thread = threading.Thread(target=orchestra, args=[client])
        thread.start()
#end main

def orchestra(client):
    print('cliente conectado')
    
    while True:
        try: 
            data = client.recv(1024)
        except:
            print("cannot receive data")
            break

        if not data: 
            break

    print('cliente desconectado')
    client.close()
#end orchestra

# =========================================
main()
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

    while True:
        client, ip = server.accept()
        thread = threading.Thread(target=orchestra, args=[client])
        thread.start()
#end main

def orchestra(client):
    print('cliente conectado')

    while True:
        try: 
            data = client.recv(258)
            msgType = data[0]
            cmdId = data[1]
            fSize = data[2]
            # msgType = int.from_bytes(data[0], 'big', signed=False)
            # cmdId = int.from_bytes(data[1], 'big', signed=False)
            # fSize = int.from_bytes(data[2], 'big', signed=False)
            fileName = data[3:].decode('utf-8')
            print(msgType, cmdId, fSize, fileName)
            print(data)

            match cmdId:
                case 3:
                    x = b'\x01\x03\x03'
                    y = 5
                    x += y.to_bytes(2, 'big', signed=False)
                    client.send(x)
                    continue

            


        except Exception as e:
            print(e)
            print("cannot receive data")
            break

        if not data: 
            break

    print('cliente perdeu a conexão')
    client.close()

main()
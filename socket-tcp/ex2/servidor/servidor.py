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
            # msgType = int.from_bytes(data[0], 'big', signed=False)
            # cmdId = int.from_bytes(data[1], 'big', signed=False)
            # fSize = int.from_bytes(data[2], 'big', signed=False)
            msgType = data[0]
            cmdId = data[1]
            fSize = data[2]
            fileName = data[3:(3+fSize)].decode('utf-8')

            print(msgType, cmdId, fSize, fileName)

            match cmdId:
                case 2:
                    handleDelete(client, fileName)
                case 3:
                    handleGFL(client)           


        except Exception as e:
            print(e)
            print("cannot receive data")
            break

        if not data: 
            break

    print('cliente perdeu a conexão')
    client.close()
#end orchestra

# ===================================
def sendRes(client, cmdId, success=False, frame=None):
    mType = int(2).to_bytes(1, 'big', signed=False)
    cmdId = cmdId.to_bytes(1, 'big', signed=False)
    sCode = int(1 if success else 2).to_bytes(1, 'big', signed=False)
    r = mType + cmdId + sCode
    if frame:
        r += frame

    client.send(r)
#end res

def handleDelete(client, filename):
    try:
        os.remove('./files/' + filename)
        sendRes(client, 2, True)
    except:
        sendRes(client, 2, False)
#end delete

def handleGFL(client):
    #get files
    files = []
    for (dirpath, dirnames, filenames) in os.walk('./files/'):
        files.extend(filenames)
        break
    
    #enviar quantidade de arquivos
    frame = len(files).to_bytes(2, 'big', signed=False)
    sendRes(client, 3, True, frame)

    #enviar o nome de cada arquivo
    for f in files:
        client.send(len(f).to_bytes(1, 'big', signed=False))
        client.send(f.encode('utf-8'))
        # client.send(frame)
#end gfl
# ===================================
main()
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

            if not data: 
                break

            # msgType = int.from_bytes(data[0], 'big', signed=False)
            # cmdId = int.from_bytes(data[1], 'big', signed=False)
            # fSize = int.from_bytes(data[2], 'big', signed=False)
            msgType = data[0]
            cmdId = data[1]
            fnSize = data[2]
            fileName = data[3:(3+fnSize)].decode('utf-8')
            if cmdId == 1:
                frame = data[(3+fnSize):(3+fnSize)+5]
                # print(frame)

            # print(msgType, cmdId, fnSize, fileName)

            match cmdId:
                case 1:
                    frame = int.from_bytes(frame, 'big', signed=False)
                    handleUpload(client, fileName, frame)
                case 2:
                    handleDelete(client, fileName)
                case 3:
                    handleGFL(client)           


        except Exception as e:
            print(e)
            print("cannot receive data")
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

def handleUpload(client, filename, fSize):
    allowed = False if os.path.exists('./files/' + filename) else True
    sendRes(client, 1, allowed)

    if allowed:
        with open('./files/' + filename, "wb") as f:
            for i in range(fSize):
                byte = client.recv(1)
                f.write(byte)
        print(f'receber arquivo {filename} ({fSize} bytes)')

        chksum = True if os.stat('./files/' + filename).st_size == fSize else False
        sendRes(client, 1, chksum)
        if not chksum:
            os.remove('./files/' + filename)
#end upload

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
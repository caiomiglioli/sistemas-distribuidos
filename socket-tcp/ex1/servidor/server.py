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
    sessionUser = None
    pwd = ''
    
    while True:
        try: 
            data = client.recv(2048).decode('utf-8')
            msgType = int(data[0])
            cmdId = int(data[1])
            frame = data[2:]

            # controle de acesso xd
            if not sessionUser:
                if not (msgType == 0 and cmdId == 0):
                    print('Usuário não logado')
                    continue

            #msg de connect,pwd,chdir,etc...
            if msgType == 0:
                match cmdId:
                    #connect
                    case 0:
                        sessionUser = handleLogin(client, frame)
                        res = 'SUCCESS' if sessionUser else 'ERROR'
                        client.send(res.encode('utf-8'))
                    
                    case 1:
                        handlePwd(client, pwd)

                    case 2:
                        p = handleChdir(client, frame, pwd)
                        if p != 'ERROR':
                            pwd = p

                    case 3:
                        handleGetfd(client, 'f', pwd)

                    case 4:
                        handleGetfd(client, 'd', pwd)

                    case 5:
                        sessionUser = None
                        client.close()
                        return print('Cliente desconectado.')
            
            #msg de getfile, addfile etc...
            elif msgType == 1:
                pass
            
            #erro
            else:
                client.send("ERROR".encode('utf-8'))

        except Exception as e:
            print(e)
            print("cannot receive data")
            break

        if not data: 
            break

    print('cliente perdeu a conexão')
    client.close()
#end orchestra

# =========================================
def handleChdir(client, path, pwd):
    fullPath = ''
    if path[0] == '/':
        fullPath = getFullPath('', path[1:])
    else:
        fullPath = getFullPath(pwd, path)

    dirExiste = None
    #if os.path.exists("demofile.txt"):
    for (dirpath, dirnames, filenames) in os.walk('./files/' + fullPath):
        dirExiste = True
        break

    if dirExiste:
        client.send('SUCCESS'.encode('utf-8'))
        return fullPath
    
    client.send('ERROR'.encode('utf-8'))
    return 'ERROR'
#end chdir

def getFullPath(pwd, path):
    fullPath = pwd.split('/') + path.split('/')
    fullPath = [dir for dir in fullPath if dir]
    
    #remove .. se for o primeiro item
    while fullPath[0] == '..':
        fullPath = fullPath[1:]

    #remove todos os .. e o diretorio anterior a ..
    i = len(fullPath)-1
    while True:
        if fullPath[i] == '..':
            fullPath.pop(i)
            fullPath.pop(i-1)
            i = i-2
        else:
            i = i-1

        if i < 0:
            break
        
    return '/'.join(fullPath)
#end getfullpath


def handlePwd(client, pwd):
    p = '/' + pwd
    client.send( p.encode('utf-8') )
#end pwd

def handleGetfd(client, type, pwd):
    items = []
    for (dirpath, dirnames, filenames) in os.walk('./files/' + pwd):
        i = dirnames if type == 'd' else filenames 
        items.extend(i)
        break

    client.send( len(items).to_bytes(4, 'big', signed=False) )

    for item in items:
        client.send( len(item).to_bytes(4, 'big', signed=False) )
        client.send( item.encode('utf-8') )
#end getdirs

def handleLogin(client, data):
    users = {"caio": "bfb37a0d503b9000bebf612b1a222479fcbd191fa69f410439f198be73d080273a57ede642afe25b6c349510c5418f1f13e1f979681a6c119e9ce46b241c5f0c",
            "ryan": "2aa60bafd5a06d8d5d450fdc723e14f25de9b9ac9bae9155a50472f27ba8768bd84857f5b7db6ebad298d2ac5e54d5fa002e41b142278db1acd8a308da2d3e18"}

    user, password = data.split('+')

    #CONNECT user,pass
    if users.get(user):
        if password == users.get(user):
            return user
    return None
#end connection

# =========================================
main()
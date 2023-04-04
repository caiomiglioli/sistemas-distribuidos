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
    sessionUser = None
    
    while True:
        try: 
            data = client.recv(2048).decode('utf-8')
            msgType = int(data[0])
            cmdId = int(data[1])
            data = data[2:]

            #controle de acesso xd
            if not sessionUser:
                if msgType and cmdId:
                    client.send("ERROR".encode('utf-8'))
                    continue

            #msg de connect,pwd,chdir,etc...
            if msgType == 0:
                match cmdId:
                    #connect
                    case 0:
                        sessionUser = handleLogin(client, data)
                        res = 'SUCCESS' if sessionUser else 'ERROR'
                        client.send(res.encode('utf-8'))

                    # case x:
                    #     sessionUser = None
                    #     client.close()
                    #     return print('Cliente desconectado.')
            
            #msg de getfile, addfile etc...
            elif msgType == 1:
                pass
            
            #erro
            else:
                client.send("ERROR".encode('utf-8'))

        except:
            print("cannot receive data")
            break

        if not data: 
            break

    print('cliente perdeu a conexão')
    client.close()
#end orchestra

def handleLogin(client, data):
    user, password = data.split('+')
    #CONNECT user,pass
    if user == 'user' and password == '5b722b307fce6c944905d132691d5e4a2214b7fe92b738920eb3fce3a90420a19511c3010a0e7712b054daef5b57bad59ecbd93b3280f210578f547f4aed4d25':
        return user
    return None
#end connection

# =========================================
main()
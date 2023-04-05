import socket

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect(('localhost', 7777))
        print('Conectado.')
    except:
        return print('\nConexão finalizada.')

    orchestra(client)
    client.close()
#end main

def orchestra(client):
    pwd = '/'
    u = 'NãoLogado'

    while True:
        cmd = input('>> ').split(' ')
        cmd[0] = cmd[0].upper()

        

        if cmd[0] == 'GETFILESLIST':
            sendReq(client, 3, '')
            handleGFL(client)

        elif cmd[0] == 'EXIT':
            # handleExit(client)
            break



def sendReq(client, cmdId, fileName):
    msgType = 1
    fSize = len(fileName)
    req = msgType.to_bytes(1, 'big', signed=False)
    req += cmdId.to_bytes(1, 'big', signed=False)
    req += fSize.to_bytes(1, 'big', signed=False)
    req += bytes(fileName, 'utf-8')
    client.send(req)

def handleGFL(client):
    try:
        data = client.recv(5)
        # data = int.from_bytes(data, 'big', signed=False)

        msgType = data[0]
        cmdId = data[1]
        sCode = data[2]
        nFile = int.from_bytes(data[3:4], 'big', signed=False)

        # if res == 'E':
        #     print('Houve um erro ao tentar buscar os diretórios.')
        # if res == 0:
        #     print('Não há diretórios no diretório corrente.')
        # elif res >= 1:
        #     print(f'Mostrando {res} diretórios:')
        #     for i in range(res):
        #         size = client.recv(4)
        #         size = int.from_bytes(size, 'big', signed=False)
        #         dir = client.recv(size).decode('utf-8')
        #         print(f'  * {dir}')
        # else:
        #     print('Resposta não reconhecida.')
        print(msgType, cmdId, sCode, nFile)
    except Exception as e:
        return print(e)


main() 
#end orchestra
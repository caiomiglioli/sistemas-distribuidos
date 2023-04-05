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
#end orchestra

# ===================================
def sendReq(client, cmdId, fileName):
    msgType = 1
    fSize = len(fileName)
    req = msgType.to_bytes(1, 'big', signed=False)
    req += cmdId.to_bytes(1, 'big', signed=False)
    req += fSize.to_bytes(1, 'big', signed=False)
    req += bytes(fileName, 'utf-8')
    client.send(req)
#end sendreq

def handleGFL(client):
    try:
        data = client.recv(5)

        msgType = data[0]
        cmdId = data[1]
        sCode = data[2]
        nFiles = int.from_bytes(data[3:5], 'big', signed=False)

        if sCode == '2':
            return print('Houve um erro ao tentar buscar os arquivos.')

        if nFiles == 0:
            print('Não há arquivos disponíveis.')
        elif nFiles >= 1:
            print(f'Mostrando {nFiles} arquivos:')
            for i in range(nFiles):
                # data = client.recv(256)
                # print('data ->', data)
                # size = data[0]
                # name = data[1:(1+size)].decode('utf-8')
                size = client.recv(1)[0]
                name = client.recv(size).decode('utf-8')
                print(f'  * {name}')
        else:
            print('Resposta não reconhecida.')

        # print(msgType, cmdId, sCode, nFiles)
    except Exception as e:
        return print(e)
#end gfl
# ===================================
main()
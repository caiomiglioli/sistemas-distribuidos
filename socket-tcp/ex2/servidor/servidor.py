"""
Este código implementa a parte servidor de um programa cliente/servidor
de armazenamento de arquivos que utiliza sockets TCP e protocolo em bytes
para comunicação.

Protocolo:

 - Solicitações:
          1 byte        1 byte           1 byte               [0 a 255] Bytes
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | Message Type | Command Ident. | Filename Size |            Filename           |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

 - Respostas:
          1 byte        1 byte           1 byte
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    | Message Type | Command Ident. |  Status Code  |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    
    + Adições (Vide PDF do enunciado)

Autores:
 - Caio Miglioli @caiomiglioli
 - Ryan Lazaretti @ryanramos01

Data de Criação: 5 de Abril de 2023
Ultima alteração: 11 de Abril de 2023
"""

import threading
import socket
import os
import logging

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.basicConfig(filename='server.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s: %(levelname)s: %(message)s')
    
    try:
        server.bind(('localhost', 7777))
        server.listen()
    except:
        return print('\nErro ao iniciar o servidor.')

    while True:
        client, ip = server.accept()
        thread = threading.Thread(target=orchestra, args=[client, ip])
        thread.start()
#end main

def orchestra(client, ip):
    """
    Função responsável por orquestrar os comandos recebidos do cliente,
    chamando as funções corretas baseadas no código do comando recebido
    no pacote do cliente.

    Esta função é executada em uma thread separada para cada usuário conectado.
    Recebe um socket 'Client' como argumento.
    """
    log('INFO', f'cliente {ip} conectado')

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
                    if handleUpload(client, fileName, frame):
                        #como o log foi feito por ultimo (pq foi esquecido haha) acabou que essa gambiarra foi feita pra resolver
                        #isso era melhor que passar o ip para cada função, mas o correto é utilizar Classe no código e guardar o client e o ip
                        #em variaveis estaticas, da classe.
                        log('INFO', f'Cliente {ip} fez o upload do arquivo {fileName}.')
                    else:
                        log('ERROR', f'Cliente {ip} falhou ao realizar o download do arquivo {fileName}.')
                    
                case 2:
                    if handleDelete(client, fileName):
                        log('INFO', f'Cliente {ip} excluiu o arquivo {fileName}.')
                    else:
                        log('ERROR', f'Cliente {ip} falhou ao excluir o arquivo {fileName}.')

                case 3:
                    handleGFL(client)
                    log('INFO', f'Cliente {ip} listou os arquivos do servidor.')

                case 4:
                    if handleDownload(client, fileName):
                        log('INFO', f'Cliente {ip} fez o download do arquivo {fileName}.')
                    else:
                        log('ERROR', f'Cliente {ip} falhou ao realizar o download do arquivo {fileName}.')


        except Exception as e:
            print(e)
            print("cannot receive data")
            break

    log('INFO', f'cliente {ip} desconectado')
    client.close()
#end orchestra

# ===================================
def sendRes(client, cmdId, success=False, frame=None):
    """
    Função responsável por enviar as respostas no protocolo correto.
    Recebe o socket 'client', o tipo do comando, e se houve sucesso para que se possa
    enviar o Status Code. E por fim o Frame, item adicional que será adicionado somente se houver conteúdo.
    """
    mType = int(2).to_bytes(1, 'big', signed=False)
    cmdId = cmdId.to_bytes(1, 'big', signed=False)
    sCode = int(1 if success else 2).to_bytes(1, 'big', signed=False)
    r = mType + cmdId + sCode
    if frame:
        r += frame

    client.send(r)
#end res

def handleDownload(client, filename):
    """
    Função responsável por realizar o envio dos arquivos do servidor para o cliente.
    Recebe o socket 'client' e o nome do arquivo.

    Checa se o arquivo existe e se sim, pega seu tamanho e coloca como frame, para o envio de resposta ao cliente.
    Logo em seguida envia byte a byte o arquivo (dessa vez sem seguir protocolo, enviando apenas o byte)
    """
    allowed = True if os.path.exists('./files/' + filename) else False

    if allowed:
        with open('./files/' + filename, "rb") as f:
            fSize = os.stat('./files/' + filename).st_size
            sendRes(client, 1, True, fSize.to_bytes(4, 'big', signed=False))
            for i in range(fSize):
                byte = f.read(1)
                client.send(byte)
        return True
    
    sendRes(client, 1, False)
    return False
#end download

def handleUpload(client, filename, fSize):
    """
    Função responsável por realizar o recebimento dos arquivos do cliente para o servidor.
    Recebe o socket 'client', o nome do arquivo 'filename', e o tamanho do arquivo 'fSize.

    Primeiro é checado se um arquivo com o mesmo nome já existe. Caso não, é enviado uma resposta
    dizendo que está tudo certo para o envio.
    Logo em seguida, é recebido byte a byte o arquivo.
    """
    allowed = False if os.path.exists('./files/' + filename) else True
    sendRes(client, 1, allowed)

    if allowed:
        with open('./files/' + filename, "wb") as f:
            for i in range(fSize):
                byte = client.recv(1)
                f.write(byte)
        print(f'recebendo arquivo {filename} ({fSize} bytes)')

        sendRes(client, 1, 'SUCCESS')
        return True
    return False
#end upload

def handleDelete(client, filename):
    """
    Função responsável por realizar a exclusão dos arquivos.
    Recebe o socket 'client', e o nome do arquivo 'filename'.
    """
    try:
        os.remove('./files/' + filename)
        sendRes(client, 2, True)
        return True
    except:
        sendRes(client, 2, False)
        return False
#end delete

def handleGFL(client):
    """
    Função responsável por enviar a lista de arquivos ao cliente.
    Recebe o socket 'client'.

    É enviado em frame a quantidade de arquivos. E para cada arquivo é enviado o tamanho de seu nome, e seu nome.
    """
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

def log(type, msg):
    if type == 'INFO':
        logging.info(msg)
    elif type == 'ERROR':
        logging.error(msg)
# ===================================


main()
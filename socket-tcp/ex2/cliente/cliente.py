"""
Este código implementa a parte cliente de um programa cliente/servidor
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
Ultima alteração: 5 de Abril de 2023
"""

import socket
import os
import time

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
    """
    Função responsável por simular o funcionamento de um terminal bash, recebendo
    comandos do usuário e chamando as funções responsáveis por tratar cada comando.
    """
    pwd = '/'
    u = 'NãoLogado'

    while True:
        cmd = input('>> ').split(' ')
        cmd[0] = cmd[0].upper()

        if cmd[0] == 'GETFILESLIST':
            handleGFL(client)

        elif cmd[0] == 'DELETE':            
            if len(cmd) < 2:
                print('Comando incompleto, tente: DELETE <filename>')
                continue
            handleDelete(client, cmd[1])

        elif cmd[0] == 'ADDFILE':
            if len(cmd) < 2:
                print('Comando incompleto, tente: ADDFILE <filename>')
                continue
            handleUpload(client, cmd[1])

        elif cmd[0] == 'GETFILE':
            if len(cmd) < 2:
                print('Comando incompleto, tente: GETFILE <filename>')
                continue
            handleDownload(client, cmd[1])

        elif cmd[0] == 'EXIT':
            # handleExit(client)
            break
#end orchestra

# ===================================
def sendReq(client, cmdId, fileName='', frame=None):
    """
    Função responsável por enviar as requisições no protocolo correto.
    Recebe o socket 'client', o tipo do comando 'cmdId', opcionalmente o nome do arquivo e um dataframe contendo
    informações específicas para cada uso (como tamanho do arquivo em ADDFILE)
    """
    msgType = 1
    fSize = len(fileName)
    req = msgType.to_bytes(1, 'big', signed=False)
    req += cmdId.to_bytes(1, 'big', signed=False)
    req += fSize.to_bytes(1, 'big', signed=False)
    req += bytes(fileName, 'utf-8')
    if frame:
        req += frame
    client.send(req)
#end sendreq

def handleDownload(client, filename):
    """
    Função responsável por realizar o recebimento dos arquivos do servidor para o cliente.
    Recebe o socket 'client', o nome do arquivo 'filename'.

    Primeiro é enviado a requisição e aguardado a resposta para poder iniciar o download.
    Caso seja permitido, é recebido o tamanho do arquivo, e então em um loop de 0 até o tamanho é
    recebido byte a byte e escrito no arquivo na pasta ./downloads/ 
    """
    sendReq(client, 4, filename)

    data = client.recv(3)
    status = data[2]
    
    if status == 1:
        duplicated = '%d'%time.time() if os.path.exists('./downloads/' + filename) else ''
        fSize = int.from_bytes(client.recv(4), 'big', signed=False)
        
        with open('./downloads/' + filename + duplicated, "wb") as f:
            for i in range(fSize):
                byte = client.recv(1)
                f.write(byte)

        print(f'Download do arquivo {filename} ({fSize} bytes) concluído')
    else:
        print('Arquivo inexistente no servidor.')
#end download

def handleUpload(client, filename):
    """
    Função responsável por realizar o envio dos arquivos do cliente para o servidor.
    Recebe o socket 'client', o nome do arquivo 'filename'.

    Primeiro é enviado a requisição contendo o nome do arquivo e seu tamanho e aguardado a resposta
    para poder iniciar o envio.
    Caso seja permitido, o arquivo é enviado byte a byte em um loop de 0 até o tamanho do arquivo e ao
    final é aguardado a resposta do servidor para saber se o arquivo foi recebido com sucesso.
    """
    try:
        with open(filename, "rb") as f:
            fSize = os.stat(filename).st_size
            sendReq(client, 1, filename, fSize.to_bytes(4, 'big', signed=False))

            res = client.recv(3)
            status = res[2]

            if status == 1:
                for i in range(fSize):
                    byte = f.read(1)
                    client.send(byte)
                
                res = client.recv(3)
                if res[2] == 1:
                    print('Arquivo enviado com sucesso!')
                else:
                    print('Erro ao fazer upload do arquivo. Tente novamente.')
    except Exception as e:
        print('Não foi possível abrir o arquivo.')
        return print(e)
#end upload

def handleDelete(client, filename):
    """
    Função responsável por realizar a exclusão dos arquivos.
    Recebe o socket 'client', e o nome do arquivo 'filename'.
    """
    sendReq(client, 2, filename)
    data = client.recv(3)
    mType = data[1]
    cmdId = data[2]
    sCode = data[2]

    if cmdId != 2 and mType != 2:
        return print('Houve um erro na operação.')
    
    if sCode == 1:
        print(f'Arquivo "{filename}" excluído com sucesso!')
    else:
        print('Houve um erro ao tentar excluir o arquivo.')

#end delete

def handleGFL(client):
    """
    Função responsável por receber a lista de arquivos do servidor.
    Recebe o socket 'client'.

    Após enviado a requisição, é recebido uma resposta com um frame adicional contendo a quantidade de
    arquivos no servidor.
    Em seguida, em um loop de 0 até a quantidade de arquivos, para cada arquivo é recebido o tamanho
    de seu nome, e logo após, seu nome.
    """
    try:
        sendReq(client, 3)
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
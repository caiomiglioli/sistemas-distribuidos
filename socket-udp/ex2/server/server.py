"""
Este código implementa a parte do servidor de um programa cliente servidor que
utiliza o protocolo UDP para comunicação para realizar upload de arquivos.

As requisições são feitas seguindo o protocolo:

    1 byte         4 bytes            1 byte                 0-254 bytes
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Command   |   File Size   |      Filename Size      |     Filename    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

Para o upload:
    1 - Requisição é feita pelo cliente
    2 - Resposta do servidor de 1 byte para confirmação
    3 - Envio do cliente de pacotes contendo bytes do arquivo seguindo o seguinte protocolo:
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
        | Numero de ordem do pacote (4bytes)  | Bytes do arquivo (0 a 1024 bytes) |
        +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    4 - Envio do cliente de um pacote contendo 40 bytes com o SHA-1 do checksum
    5 - Resposta do servidor de 1 byte para resultado da comparação do checksum


Autores:
 - Caio Miglioli @caiomiglioli
 - Ryan Lazaretti @ryanramos01

Data de Criação: 18 de Abril de 2023
Ultima alteração: 18 de Abril de 2023    
"""

import socket
import os
import math
import hashlib


def server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('localhost', 7777))

    while (True):
        [request, client] = server.recvfrom(260)
        cmd = request[0] 

        match cmd:
            #upload
            case 0:
                handleUpload(server, client, request)
#end main

def handleUpload(server, client, request):
    fSize = int.from_bytes(request[1:5], "big")
    fnSize = request[5]
    filename = request[6:(6+fnSize)].decode("utf-8")

    #checar se pode enviar (se existe arquivo repetido, etc...)
    # allowed = 0 if os.path.exists('./files/' + filename) else 1
    allowed = 1
    res = allowed.to_bytes(1, 'big', signed=False)        
    server.sendto(res, client)
    
    if not allowed:
        return False
    
    packets = math.ceil(fSize/1024)
    # packetsControl = [i for i in range(packets)]

    with open('./files/' + filename, "wb") as f:
        for i in range(packets):
            [dgram, c] = server.recvfrom(1028)
            if c != client:       
                server.sendto(int(0).to_bytes(1, 'big', signed=False), c)
                continue
            
            index = int.from_bytes(dgram[0:4], "big")
            content = dgram[4:]

            try:
                f.seek(index*1024)
                f.write(content)
                # packetsControl.remove(index)
            except:
                print(f'Erro no pacote {index}')
        #end primary for

        #pode ser usado para recuperar pacotes perdidos (mas n vou implementar xd)
        # print(packetsControl)
    #end open

    # checksum hash
    [dgram, c] = server.recvfrom(40)

    with open('./files/' + filename, "rb") as f:
        file = f.read()
        chksum = hashlib.sha1(file)
    
    chksumResult = 1 if dgram.decode('utf-8') == chksum.hexdigest() else 0
    server.sendto(chksumResult.to_bytes(1, 'big', signed=False), client)

    print(filename, dgram.decode('utf-8'), chksum.hexdigest())
#end upload

# =======================================
if __name__ == '__main__':
    server()
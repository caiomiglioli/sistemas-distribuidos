import socket
import os
import math
import hashlib


def client():
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    server = ('localhost', 7777)

    while True:
        cmd = input('>> ').split(' ')

        if cmd[0] == 'EXIT':
            break
        elif cmd[0] == 'ADDFILE':
            if len(cmd) < 2:
                print("Comando incompleto. Tente 'ADDFILE <nome-do-arquivo>")
                continue
            handleUpload(client, server, cmd[1])
#end main

def handleUpload(client, server, filename):

    try:
        with open(filename, "rb") as f:
            cmd = 0
            fSize = os.stat(filename).st_size
            fnSize = len(filename)
            req = cmd.to_bytes(1, 'big', signed=False) + fSize.to_bytes(4, 'big', signed=False) + fnSize.to_bytes(1, 'big', signed=False) + bytes(filename, 'utf-8')
            client.sendto(req, server)

            [allowed, _] = client.recvfrom(1)

            if allowed[0] != 1:
                return print('Erro ao enviar o arquivo. Tente novamente mais tarde.')
            
            packets = math.ceil(fSize/1024)
            for i in range(packets):
                pNumber = i.to_bytes(4, 'big', signed=False)
                content = f.read(1024)
                packet = pNumber + content
                client.sendto(packet, server)
        #end open

        # hash
        with open(filename, "rb") as f:
            file = f.read()
            chksum = hashlib.sha1(file)
            client.sendto(bytes(chksum.hexdigest(), 'utf-8'), server)
        
        [success, _] = client.recvfrom(1)
        if success[0] != 1:
            return print('Erro ao enviar o arquivo. Tente novamente mais tarde.')
        return print('Arquivo enviado com sucesso!')

    except Exception as e:
        print('Não foi possível abrir o arquivo.')
        return print(e)

#end upload

# =======================================
if __name__ == '__main__':
    client()
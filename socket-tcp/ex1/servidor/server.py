"""
Este código implementa a parte servidor de um programa cliente/servidor
de gerenciamento de arquivos que utiliza sockets TCP e formato string
utf-8 para comunicação.

Autores:
 - Caio Miglioli @caiomiglioli
 - Ryan Lazaretti @ryanramos01

Data de Criação: 3 de Abril de 2023
Ultima alteração: 11 de Abril de 2023
"""

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

    # Para cada nova conexão, é gerado uma thread que executa a função
    # 'orchestra', que por sua vez, aguarda os comandos do cliente.
    while True:
        client, ip = server.accept()
        thread = threading.Thread(target=orchestra, args=[client])
        thread.start()
#end main

def orchestra(client):
    """
    Função responsável por orquestrar os comandos recebidos do cliente,
    chamando as funções corretas baseadas no código do comando recebido
    no pacote do cliente.

    Esta função é executada em uma thread separada para cada usuário conectado.
    Recebe um socket 'Client' como argumento.
    """

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
    """
    Função responsável por tratar o comando de troca de diretório no servidor.
    Recebe como argumentos o socket 'Client', o caminho 'path' em que se deseja navegar, e o caminho 'pwd' atual do usuário.
    Em caso de sucesso retorna o novo caminho 'pwd' para que se possa ser utilizado em outros comandos.
    """        
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
    """
    Função auxiliar para o CHDIR.
    Junta o PWD e PATH em uma array, e para cada '..' encontrado, remove o item anterior,
    executando o comando de voltar ao diretório anterior
    """
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
    """
    Função responsável por tratar o comando para saber o caminho do diretório atual.
    Recebe como argumentos o socket 'Client' e o path atual do servidor 'pwd'.
    """
    p = '/' + pwd
    client.send( p.encode('utf-8') )
#end pwd

def handleGetfd(client, type, pwd):
    """
    Função responsável por tratar o comando que exibe os diretórios ou os arquivos contidos no diretório atual.
    Recebe como argumentos o socket 'Client', o 'type' que indica se é pra buscar arquivos ou diretórios, e
    o 'pwd' que indica o diretório atual do servidor.

    Primeiro é descoberto os itens (de acordo com o type), então é enviado a quantidade de itens, e depois
    em um laço de 0 até a quantidade, em cada iteração, é enviado o tamanho do nome do item e logo em seguida
    seu nome.
    """
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
    """
    Função responsável por tratar o comando de login.
    Recebe como argumentos o socket 'Client' e a string 'user+password' em 'data'.
    Em caso de sucesso, retorna o usuário para que a função 'Orchestra' saiba que há uma sessão logada.
    """
    # Para evitar o uso e configuração de um banco de dados em um programa cujo intuito não é
    # trabalhar estes aspectos, os usuários foram gerados hardcoded
    users = {
        "caio": "bfb37a0d503b9000bebf612b1a222479fcbd191fa69f410439f198be73d080273a57ede642afe25b6c349510c5418f1f13e1f979681a6c119e9ce46b241c5f0c",
        "ryan": "2aa60bafd5a06d8d5d450fdc723e14f25de9b9ac9bae9155a50472f27ba8768bd84857f5b7db6ebad298d2ac5e54d5fa002e41b142278db1acd8a308da2d3e18"
    }

    user, password = data.split('+')
    #CONNECT user,pass
    if password == users.get(user):
        client.send('SUCCESS'.encode('utf-8'))
        return user

    client.send('ERROR'.encode('utf-8'))
    return None
#end connection

# =========================================
main()
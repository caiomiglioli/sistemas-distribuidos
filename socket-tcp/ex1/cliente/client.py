"""
Este código implementa a parte cliente de um programa cliente/servidor
de gerenciamento de arquivos que utiliza sockets TCP e formato string
utf-8 para comunicação.

Autores:
 - Caio Miglioli @caiomiglioli
 - Ryan Lazaretti @ryanramos01

Data de Criação: 3 de Abril de 2023
Ultima alteração: 4 de Abril de 2023
"""

import socket
from hashlib import sha512

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect(('localhost', 7777))
        print('Conectado.')
    except:
        return print('\nConexão finalizada.')

    try:
        orchestra(client)
    except:
        print('Alguma coisa deu errado!')
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
        cmd = input(f'{u}:{pwd} >> ').split(' ')
        cmd[0] = cmd[0].upper()

        #inicio tipo de msg 0
        if cmd[0] == 'CONNECT':
            if len(cmd) < 2:
                print('Comando incompleto, tente: CONNECT <user>,<password>')
                continue
            res = handleLogin(client, cmd[1])
            if res:
                u = res            
        
        elif cmd[0] == 'EXIT':
            handleExit(client)
            break
        
        elif u == 'NãoLogado':
            print('Comando não permitido.')

        elif cmd[0] == 'PWD':
            pwd = handlePwd(client)
        
        elif cmd[0] == 'CHDIR':
            if len(cmd) < 2:
                print('Comando incompleto, tente: CHDIR <path>')
                continue
            p = handleChdir(client, cmd[1])
            if p:
                pwd = p
        
        elif cmd[0] == 'GETFILES':
            handleGetfiles(client)
        
        elif cmd[0] == 'GETDIRS':
            handleGetdirs(client)
        
        #fim tipo de mensagem 0
        #inicio tipo de mensagem 1
        else:
            print('Comando inválido!')
#end orchestra

# ===========================================

def handleChdir(client, path):
    """
    Função responsável por tratar o comando de troca de diretório no servidor.
    Recebe como argumentos o socket 'Client' e o caminho 'path' em que se deseja navegar.
    Em caso de sucesso retorna o novo caminho para que se possa exibir no bash.
    """
    try:
        req = '02' + path # código do comando + dataframe
        client.send(req.encode('utf-8'))
        res = client.recv(1024).decode('utf-8')

        if res == 'SUCCESS':
            return handlePwd(client)
        else:
            print('Não foi possível navegar ao diretório.')

    except Exception as e:
        return print(e)
#end chdir

def handlePwd(client):
    """
    Função responsável por tratar o comando para saber o caminho do diretório atual.
    Recebe como argumentos o socket 'Client' e em caso de sucesso retorna o caminho
    para que se possa exibir no bash.
    """
    try:
        client.send('01'.encode('utf-8'))
        res = client.recv(2048).decode('utf-8')
        print(f'Diretório atual: {res}')
        return res

    except Exception as e:
        return print(e)
#end pwd    

def handleGetfiles(client):
    """
    Função responsável por tratar o comando que exibe os arquivos do diretório atual.
    Recebe como argumentos o socket 'Client'.

    É enviado o código do comando, recebido a quantidade de arquivos, e depois em um
    laço de 0 até a quantidade recebida, em cada iteração é recebido o tamanho do nome 
    de um arquivo e logo em seguida seu nome.
    """
    try:
        client.send('03'.encode('utf-8'))
        res = client.recv(4)
        res = int.from_bytes(res, 'big', signed=False)

        # if res == 'E':
        #     print('Houve um erro ao tentar buscar os diretórios.')
        if res == 0:
            print('Não há arquivos no diretório corrente.')
        elif res >= 1:
            print(f'Mostrando {res} arquivos:')
            for i in range(res):
                size = client.recv(4)
                size = int.from_bytes(size, 'big', signed=False)
                arq = client.recv(size).decode('utf-8')
                print(f'  * {arq}')
        else:
            print('Resposta não reconhecida.')
    except Exception as e:
        return print(e)
#end getfiles

def handleGetdirs(client):
    """
    Função responsável por tratar o comando que exibe os diretórios contidos no diretório atual.
    Recebe como argumentos o socket 'Client'.

    É enviado o código do comando, recebido a quantidade de diretórios, e depois em um
    laço de 0 até a quantidade recebida, em cada iteração é recebido o tamanho do nome 
    de um diretório e logo em seguida seu nome.
    """
    try:
        client.send('04'.encode('utf-8'))
        res = client.recv(4)
        res = int.from_bytes(res, 'big', signed=False)

        # if res == 'E':
        #     print('Houve um erro ao tentar buscar os diretórios.')
        if res == 0:
            print('Não há diretórios no diretório corrente.')
        elif res >= 1:
            print(f'Mostrando {res} diretórios:')
            for i in range(res):
                size = client.recv(4)
                size = int.from_bytes(size, 'big', signed=False)
                dir = client.recv(size).decode('utf-8')
                print(f'  * {dir}')
        else:
            print('Resposta não reconhecida.')
    except Exception as e:
        return print(e)
#end getdirs

def handleExit(client):
    """
    Envia um sinal para que o servidor feche o socket.
    Fecha o socket local. (O terminal é fechado na função 'orchestra')
    """
    req = '05'
    try:
        client.send(req.encode('utf-8'))
        client.close()
        print('Desconectado')
    except:
        print("Algo deu errado.")
#end exit

def handleLogin(client, data):
    """
    Função responsável por tratar o comando de login.
    Recebe como argumentos o socket 'Client' e a string 'nome,senha' em 'data'.
    Em caso de sucesso, retorna o usuário para exibição no terminal.
    
    É enviado o código do comando, o usuário, o divisor (+) e a senha criptografada
    em sha512.
    """
    user, password = data.split(',')
    password = sha512(password.encode('utf-8')).hexdigest()
            
    # 0 = codigo de tipo de mensagem, 
    req = '00' + user + '+' + password
    res = None
    try:
        print('Realizando login...')
        client.send(req.encode('utf-8'))
        res = client.recv(2048).decode('utf-8')
    except:
        raise Exception('Falha no login')

    if res == 'SUCCESS':
        print('Logado com sucesso!')
        return user
    else:
        print('Usuário ou senha incorreto.')
        return None
#end login
# =========================================
main()
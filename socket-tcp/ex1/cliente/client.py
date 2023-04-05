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
    try:
        req = '02' + path
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
    try:
        client.send('01'.encode('utf-8'))
        res = client.recv(2048).decode('utf-8')
        print(f'Diretório atual: {res}')
        return res

    except Exception as e:
        return print(e)
#end pwd    

def handleGetfiles(client):
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
    req = '05'
    try:
        client.send(req.encode('utf-8'))
        client.close()
        print('Desconectado')
    except:
        print("Algo deu errado.")
#end exit

def handleLogin(client, data):
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
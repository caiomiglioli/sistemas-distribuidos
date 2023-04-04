import socket
from hashlib import sha512

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect(('localhost', 7777))
    except:
        return print('\nConexão finalizada.')

    try:
        orchestra(client)
    except:
        print('Alguma coisa deu errado!')
        client.close()
#end main

def orchestra(client):
    while True:
        cmd = input('>').split(' ')
        
        if cmd[0] == 'exit':
            print('\nDesconectado')
            client.close()
            break
        
        elif cmd[0] == 'CONNECT':
            if len(cmd) < 2:
                print('Comando incompleto, tente: CONNECT <user>,<password>')
                continue

            user, password = cmd[1].split(',')
            password = sha512(password.encode('utf-8')).hexdigest()
            
            # 0 = codigo de tipo de mensagem, 
            req = '00' + user + '+' + password
            res = None
            try:
                print('Conectando...')
                client.send(req.encode('utf-8'))
                res = client.recv(2048).decode('utf-8')
                print('DEBUG res', res)
            except:
               raise Exception('Falha no login')

            if res == 'SUCCESS':
                print('Logado com sucesso!')
            else:
                print('Usuário ou senha incorreto.')

        else:
            print('Comando inválido!')
#end orchestra

# =========================================
main()
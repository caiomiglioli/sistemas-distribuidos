import socket

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
            print('conectando...')
        
        else:
            print('Comando inválido!')
#end orchestra

# =========================================
main()
import socket
import sys
import os

# Global Variables
REQ_CODE = 1
RESP_CODE = 2

COMMANDS_CODES = {
    'DEFAULT': 0,
    'ADDFILE': 1,
    'DELETE': 2,
    'GETFILESLIST': 3,
    'GETFILE': 4,
    'EXIT': 5,
    1: 'ADDFILE',
    2: 'DELETE',
    3: 'GETFILESLIST',
    4: 'GETFILE',
    5: 'EXIT',
    0: 'DEFAULT'
}

STATUS_CODE = {
    'SUCCESS': 1,
    'ERROR': 2,
    1: 'SUCCESS',
    2: 'ERROR'
}

BYTEORDER = 'big'
LOCAL_CLIENT = ''


def build_request_message(message):
    command = message.split()[0]

    req_message = REQ_CODE.to_bytes(1, BYTEORDER)
    req_message += COMMANDS_CODES.get(command, 0).to_bytes(1, BYTEORDER)

    file_name = ''
    if command in ['ADDFILE', 'DELETE', 'GETFILE']:
        file_name = message.split()[1]

    req_message += len(file_name).to_bytes(1, BYTEORDER)
    req_message += bytes(file_name, 'utf-8')

    return command, req_message, file_name


def send_data(clientsocket, message):
    command, req_message, file_name = build_request_message(message)

    if command == 'ADDFILE':
        file_size = os.path.getsize(file_name)
        req_message += file_size.to_bytes(4, BYTEORDER)

        with open(file_name, 'rb') as file_to_send:
            for data in file_to_send:
                req_message += data
                clientsocket.send(req_message)
                req_message = bytes()

    else:
        clientsocket.send(req_message)


def connect_to_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ['localhost', 10100]
    print(f'connecting to {server_address[0]} port {server_address[1]}')
    sock.connect(tuple(server_address))

    return sock


def main_loop(sock):
    prefix = 'CLIENT >>'

    while True:
        message = input(f'{prefix} ')

        send_data(sock, message)

        server_message = ''
        resp_message = sock.recv(1024)

        resp_command = int.from_bytes(resp_message[1:2], BYTEORDER)
        resp_status = int.from_bytes(resp_message[2:3], BYTEORDER)

        command_name = COMMANDS_CODES[resp_command]
        
        if command_name == 'EXIT':
            break
        elif command_name == 'DELETE':
            server_message = 'Arquivo deletado com sucesso!' if STATUS_CODE[resp_status] == 'SUCCESS' else 'O arquivo solicitado não pode ser deletado.'
        elif command_name == 'GETFILESLIST':
            server_message = process_getfilelist_response(resp_message, sock)
        elif command_name == 'GETFILE':
            server_message = process_getfile_response(resp_message, message, sock)
        elif command_name == 'ADDFILE':
            server_message = 'Arquivo enviado com sucesso!'
        else:
            server_message = 'A requisição não pode ser concluída.'

        print(f'SERVER >> {server_message}')


def process_getfilelist_response(resp_message, sock):
    server_message = ''
    number_files = int.from_bytes(resp_message[3:5], BYTEORDER)

    namefile_size = int.from_bytes(resp_message[5:6], BYTEORDER)
    namefile = resp_message[6:6+ namefile_size].decode('utf-8')
    server_message += f'\n\t{namefile}\n'

    for index in range(number_files - 1):
        resp_message = sock.recv(1024)
        namefile_size = int.from_bytes(resp_message[5:6], BYTEORDER)
        namefile = resp_message[6:6 + namefile_size].decode('utf-8')
        server_message += f'\t{namefile}' if index == number_files - 2 else f'\t{namefile}\n'

    return server_message


def process_getfile_response(resp_message, message, sock):
    resp_status = int.from_bytes(resp_message[2:3], BYTEORDER)

    if STATUS_CODE[resp_status] == 'SUCCESS':
        server_message = 'Arquivo baixado com sucesso!'

        bytes_received = 0
        file_size = int.from_bytes(resp_message[3:7], BYTEORDER)

        data_write = resp_message[7:]
        bytes_received += len(data_write)

        with open(os.path.join(LOCAL_CLIENT, message.split()[1]), 'wb') as file_to_write:
            file_to_write.write(data_write)

            while bytes_received < file_size:
                resp_message = sock.recv(1024)
                data_write = resp_message
                bytes_received += len(data_write)
                file_to_write.write(data_write)

    else:
        server_message = 'O arquivo solicitado não pode ser baixado.'

    return server_message


if __name__ == '__main__':
    LOCAL_CLIENT = os.getcwd()

    sock = connect_to_server()
    main_loop(sock)

    print(f'closing socket')
    sock.close()
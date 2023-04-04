import copy
import socket
import sys
import threading
import os
from datetime import datetime


# Global variables
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
LOCAL_SERVER = ''


def handle_client(clientsocket, addr):
    global LOCAL_SERVER
    print(f'Connection established with {addr}')

    while True:
        req_message = clientsocket.recv(1024)
        print(f'{addr} >> {req_message}')

        message_type = req_message[0:1]
        command = req_message[1:2]
        filename_size = req_message[2:3]
        filename = req_message[3:(3 + int.from_bytes(filename_size, BYTEORDER))]

        log_request(addr, message_type + command + filename_size + filename)

        resp_message = build_response_message(command, filename)
        clientsocket.send(resp_message)

        if COMMANDS_CODES[int.from_bytes(command, BYTEORDER)] == 'EXIT':
            break

    clientsocket.close()


def log_request(addr, message):
    with open("history.log", "a") as file_object:
        message_log = f'{datetime.now()} {addr} >> {message}\n'
        file_object.write(message_log)


def build_response_message(command, filename):
    command_name = COMMANDS_CODES[int.from_bytes(command, BYTEORDER)]
    response = RESP_CODE.to_bytes(1, BYTEORDER)
    response += int.from_bytes(command, BYTEORDER).to_bytes(1, BYTEORDER)

    if command_name == 'DELETE':
        response += handle_delete(filename)

    elif command_name == 'GETFILESLIST':
        response += handle_get_files_list()

    elif command_name == 'GETFILE':
        response += handle_get_file(filename)

    elif command_name == 'ADDFILE':
        response += handle_add_file(filename)

    else:
        response += STATUS_CODE['ERROR'].to_bytes(1, BYTEORDER)

    return response


def handle_delete(filename):
    if os.path.isfile(filename.decode('utf-8')):
        os.remove(filename.decode('utf-8'))
        return STATUS_CODE['SUCCESS'].to_bytes(1, BYTEORDER)
    else:
        return STATUS_CODE['ERROR'].to_bytes(1, BYTEORDER)


def handle_get_files_list():
    response = STATUS_CODE['SUCCESS'].to_bytes(1, BYTEORDER)

    files = os.listdir(LOCAL_SERVER)
    response += len(files).to_bytes(2, BYTEORDER)

    for index, file in enumerate(files):
        repeatable_resp_message = copy.deepcopy(response)
        repeatable_resp_message += len(file).to_bytes(1, BYTEORDER)
        repeatable_resp_message += bytes(file, 'utf-8')

    return repeatable_resp_message


def handle_get_file(filename):
    if os.path.isfile(filename):
        response = STATUS_CODE['SUCCESS'].to_bytes(1, BYTEORDER)

        file_size = os.path.getsize(filename.decode('utf-8'))
        response += file_size.to_bytes(4, BYTEORDER)

        with open(filename.decode('utf-8'), 'rb') as file_to_send:
            for data in file_to_send:
                response += data

        return response

    else:
        error_response = STATUS_CODE['ERROR'].to_bytes(1, BYTEORDER)
        error_response += (0).to_bytes(4, BYTEORDER)
        error_response += bytes(0)
        return error_response


def handle_add_file(filename):
    response = STATUS_CODE['SUCCESS'].to_bytes(1, BYTEORDER)

    bytes_received = 0
    i_index = 3 + int.from_bytes(filename, BYTEORDER)
    f_index = i_index + 4
    file_size = int.from_bytes(req_message[i_index:f_index], BYTEORDER)

    data_write = req_message[f_index:]
    bytes_received += len(data_write)

    with open(os.path.join(LOCAL_SERVER, filename.decode('utf-8')), 'wb') as file_to_write:
        file_to_write.write(data_write)

        while bytes_received < file_size:
            req_message = clientsocket.recv(1024)
            data_write = req_message
            bytes_received += len(data_write)
            file_to_write.write(data_write)

    return response


if __name__ == '__main__':

    LOCAL_SERVER = os.getcwd()

    # Create TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to its TCP port
    server_address = ('localhost', 10100)
    print(f'starting up on {server_address[0]} port {server_address[1]}')
    sock.bind(server_address)

    # Listen for connections
    print('waiting for a connection')
    sock.listen(1)

    # Create a thread for each new connection
    while True:
        connection, client_address = sock.accept()
        client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
        client_thread.start()
"""
Este código implementa um chat P2P que utiliza sockets UDP para comunicação.

Autores:
 - Ryan Lazaretti @ryanramos01
 - Caio Miglioli @caiomiglioli

Data de Criação: 11 de Abril de 2023
Ultima alteração: 11 de Abril de 2023
"""

import socket
import threading
import re
import emoji

# Define o número do código dos tipos das mensagens.
NORMAL_MESSAGE = 1
STICKER_MESSAGE = 2
URL_MESSAGE = 3
ECHO_MESSAGE = 4


# Recebe as informações do usuário como, nickname, ip de conexão e porta UDP que será o acesso.
def inputUser():
    nickName = input("Nick: ")
    if nickName == "":
        nickName = "DefaultUser"

    # Padrão LOCALHOST = 127.0.0.1
    addressConnect = input("IP de conexão (Deixe em branco para LOCALHOST): ")
    if addressConnect == "":
        addressConnect = "127.0.0.1"

    portConnect = int(input("UDP portConnect: "))

    return nickName, addressConnect, portConnect


def recive_message(sock):
    while True:
        # Recebe a menssagem.
        (data, address) = sock.recvfrom(1024)

        # Decodifica a menssagem recebida.
        typeMessage = int.from_bytes(data[0:1], "big")
        sizeNick = int.from_bytes(data[1:2], "big")
        nickName = data[2 : (sizeNick + 2)].decode("utf-8")
        sizeMessage = int.from_bytes(data[(sizeNick + 2) : (sizeNick + 3)], "big")
        message = ""

        # Atribui o valor correto à variável message.
        if sizeMessage > 0:
            message = data[(sizeNick + 3) : (sizeNick + 3 + sizeMessage)].decode(
                "utf-8"
            )

        # Se a mensagem recebida for do tipo ECHO, retorna a mesma mensagem.
        if typeMessage == ECHO_MESSAGE:
            echoMessage = message[5:]
            header = dataBuilder(echoMessage, nickName)
            sock.sendto(header, address)
        # Emojis suportados https://carpedm20.github.io/emoji/all.html?enableList=enable_list_pt
        elif typeMessage == STICKER_MESSAGE:
            print(
                emoji.emojize(
                    "{}: {}".format(nickName, message),
                    language="pt",
                )
            )
        else:
            print("{}: {}".format(nickName, message))


# Checka se a mensagem recebida é um STICKER.
def isSticker(message):
    if message[0] == ":" and message[-1] == ":":
        return True

    return False


# Checka se a mensagem recebida é uma URL.
def isURL(message):
    regexURL = re.compile(r"^(http|https|ftp)://[^\s]+")

    return bool(regexURL.match(message))


# Checka se a mensagem recebida é um ECHO.
def isECHO(message):
    echoMessage = message.split()
    if echoMessage[0] == "ECHO":
        return True

    return False


# Faz a montagem do cabeçalho codificando para bytes.
def dataBuilder(message, nickName):
    # Define o tipo da menssagem recebida
    if isSticker(message):
        typeMessage = STICKER_MESSAGE
    elif isURL(message):
        typeMessage = URL_MESSAGE
    elif isECHO(message):
        typeMessage = ECHO_MESSAGE
    else:
        typeMessage = NORMAL_MESSAGE

    # Cria o cabeçalho no formato do enunciado.
    data = typeMessage.to_bytes(1, "big")
    data += len(nickName).to_bytes(1, "big")
    data += bytes(nickName, "utf-8")
    data += len(message).to_bytes(1, "big")
    data += bytes(message, "utf-8")

    return data


# MAIN
if __name__ == "__main__":
    # Chama a função inputUser para obter informações do usuário.
    nickName, ipConnect, portConnect = inputUser()

    # Cria um socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Define os endereços do servidor e de escuta.
    server_address = (ipConnect, portConnect)
    listen_address = (ipConnect, (portConnect + 1))

    try:
        # Tenta vincular o socket à porta de escuta.
        sock.bind(listen_address)
        print("Server UP")

    except OSError:
        # Se a porta já estiver em uso, vincula o socket à porta do servidor.
        listen_address = server_address
        server_address = (ipConnect, (portConnect + 1))
        sock.bind(listen_address)

    # Cria uma nova thread para receber mensagens.
    client_socket = threading.Thread(target=recive_message, args=(sock,))
    client_socket.start()

    while True:
        # Lê a entrada do usuário.
        message = input(f"{nickName}: ")

        # Verifica se a entrada é uma string vazia ou apenas contém espaços em branco.
        if message == "" or message.isspace():
            continue

        # Cria a mensagem para enviar ao servidor.
        data = dataBuilder(message, nickName)

        # Envia a mensagem para o servidor.
        sock.sendto(data, server_address)

Programação com sockets TCP

Autores:
 - Caio Miglioli @caiomiglioli
 - Ryan Lazaretti @ryanramos01

======================================================
Exercicio 1:

>Como compilar
    Não é necessário compilar

>Como executar
    É necessário executar o servidor primeiro.
    - Servidor:
        $ python ./ex1/servidor/server.py
    - Cliente:
        $ python ./ex1/cliente/client.py

>Bibliotecas usadas (descrever as não padrões)
    - os: Biblioteca do Python para executar comandos do sistema.
    - hashlib: Biblioteca que implementa funções de criptografia.
    - threading: Biblioteca que implementa threads no Python.

>Exemplo de uso
    No terminal do cliente:
        $ CONNECT caio,2135523
        $ GETDIRS
        $ CHDIR images
        $ GETFILES
        $ DELETE xd.txt
        $ GETFILES
        $ CHDIR ..
        $ PWD


======================================================
Exercicio 2:

>Como compilar
    Não é necessário compilar

>Como executar
    É necessário executar o servidor primeiro.
    - Servidor:
        $ python ./ex2/servidor/servidor.py
    - Cliente:
        $ python ./ex2/cliente/cliente.py

>Bibliotecas usadas (descrever as não padrões)
    - os: Biblioteca do Python para executar comandos do sistema.
    - hashlib: Biblioteca que implementa funções de criptografia.
    - threading: Biblioteca que implementa threads no Python.

>Exemplo de uso
    No terminal do cliente:
        $ GETFILESLIST
        $ ADDFILE teste.txt
        $ GETFILESLIST
        $ DELETE x.txt
        $ GETFILESLIST
        $ GETFILE foto.jpg
    Checar foto baixada em ./ex2/cliente/downloads
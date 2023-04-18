Programação com sockets UDP

Autores:
 - Caio Miglioli @caiomiglioli
 - Ryan Lazaretti @ryanramos01

======================================================
Exercicio 1:

>Como compilar
    Não é necessário compilar

>Como executar
    - É necessário instalar a biblioteca 'EMOJI'
        $ pip install emoji
    - Em dois terminais diferentes execute:
        $ python ./ex1/chatP2P.py

>Bibliotecas usadas (descrever as não padrões)
    - os: Biblioteca do Python para executar comandos do sistema.
    - re: Biblioteca que implementa funções de regex.
    - threading: Biblioteca que implementa threads no Python.
    - emoji: Biblioteca que implementa a exibição de emoticons no terminal

>Exemplo de uso
    No primeiro terminal, após executar o programa:
        - Digite o nickname
        - Deixe o IP em branco
        - Digite 7777 como número da porta

    No segundo terminal, após executar o programa:
        - Digite o nickname
        - Deixe o IP em branco
        - Digite 7777 como número da porta

    Em qualquer terminal:
        $ <nickname>: olá
        $ <nickname>: :Brazil:
        $ <nickname>: ECHO teste

======================================================
Exercicio 2:

>Como compilar
    Não é necessário compilar

>Como executar
    - Servidor:
        $ python ./ex2/server/server.py
    - Cliente:
        $ python ./ex2/client/client.py

>Bibliotecas usadas (descrever as não padrões)
    - os: Biblioteca do Python para executar comandos do sistema.
    - hashlib: Biblioteca que implementa funções de criptografia.

>Exemplo de uso
    No terminal do cliente:
        $ ADDFILE foto.jpg
    Checar foto enviada em ./ex2/server/files
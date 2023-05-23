Programação com RPC

Autores:
 - Caio Miglioli @caiomiglioli
 - Ryan Lazaretti @ryanramos01

======================================================

>Como compilar
    Server:
        $ cd server
        $ python -m grpc_tools.protoc -I../protos --python_out=. --pyi_out=. --grpc_python_out=. ../protos/movies.proto
        $ pip install -r requirements.txt

    Client:
        $ npm install
        (O próprio framework do gRPC se encarrega de compilar o protobuf)


>Como executar
    É necessário executar o servidor primeiro.
    - Servidor:
        $ python ./server/server.py
    - Cliente:
        $ node ./client/client.js

>Bibliotecas usadas (descrever as não padrões)
    - concurrent.futures: Permite o servidor a criar threads que serão criadas para cada conexão

>Exemplo de uso
    No terminal do cliente:
        > ListByGenre Animation
        > ListByActor James
        > Create
            (Será pedido uma sequencia de inputs para criar cada campo)
        > Read Regeneration
        > Update 573a1390f29313caabcd516c
            (Será pedido uma sequencia de inputs para editar cada campo)
        > Delete 573a1390f29313caabcd516c

    Comandos disponíveis:
        ListByActor <Actor Name>
        ListByGenre <Genre Name>
        Create
        Read <Movie Title>
        Update <Movie Id>
        Delete <Movie Id>
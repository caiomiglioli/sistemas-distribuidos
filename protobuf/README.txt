Programação com Representação Externa de Dados

Autores:
 - Caio Miglioli @caiomiglioli
 - Ryan Lazaretti @ryanramos01

======================================================
Exercicio 1:

>Como compilar
    Protobuf:
        protoc movies.proto --python_out=./server/
        protoc -I=. --js_out=import_style=commonjs:. --grpc-web_out=import_style=commonjs,mode=grpcwebtext:. movies.proto

    Server:
        pip install pymongo pprint protobuf

    Client:
        npm install prompt-sync promise-socket google-protobuf


>Como executar
    É necessário executar o servidor primeiro.
    - Servidor:
        $ python ./server/server.py
    - Cliente:
        $ node ./client/client.js

>Bibliotecas usadas (descrever as não padrões)
    - promise-socket: Permite utilizar Async-Await com os sockets no nodejs

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
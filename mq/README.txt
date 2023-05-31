Programação com Comunicação Indireta

Autores:
 - Caio Miglioli @caiomiglioli
 - Ryan Lazaretti @ryanramos01

======================================================

>Como compilar
    - É necessário instalar as dependências.
        $ pip install -r requirements.txt
        $ cd client && npm install


>Como executar
    - É necessário executar o servidor RabbitMQ primeiro.
    >> Os comandos de como executar está no arquivo 'rabbitmq-docker'

    * Não importa a ordem:
    - Coletor:
        $ python ./colector/colector.py
    - Classificador
        $ python ./classifier/classifier.py
    - Cliente:
        $ node ./client/client.js


>Bibliotecas usadas (descrever as não padrões)
    - spicy: Biblioteca de processamento de linguagem natural que permite remover as stop-words de um texto.
    - pika (python): Permite o classificador e coletor a conectarem e se comunicarem com o servidor RabbitMQ
    - amqplib (Node): Permite o cliente a conectar e se comunicar com o servidor RabbitMQ 


>Exemplo de uso
    No terminal do cliente:
        > culture news

    Topicos disponíveis:
        culture
        news
        tech
        sports
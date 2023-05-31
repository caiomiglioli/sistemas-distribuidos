"""
Este código implementa a parte Coletora de um programa de fila de mensagens que coleta,
classifica e distribui tweets de acordo com tópicos selecionados pelo cliente.

Autores:
  - Caio Miglioli @caiomiglioli
  - Ryan Lazaretti @ryanramos01

Data de Criação: 30 de Maio de 2023
Ultima alteração: 31 de Maio de 2023
"""

import pika
from json import dumps
from csv import reader
from time import sleep

def tw2dict(header, tw):
    """
    Recebe um vetor header contendo o nome de cada coluna do csv
    Recebe um vetor tw contendo os valores de uma coluna qualquer do csv
    Junta ambos em um dicionário chave-valor e retorna
    """
    res = dict()
    for i, head in enumerate(header):
        res[head] = tw[i]
    return res


def publishFromCSV(filename, channel, interval):
    """
    Função que lê cada linha do CSV, e coordena a publicação chamando as funções necessárias (tw2dict e publish)
    """
    with open(filename, newline='') as tws:
        _reader = reader(tws)
        header = None

        for i, tw in enumerate(_reader):
            # if i > 1: break #enviar somente 1 tweet xd
            
            if i == 0:
                header = tw
                continue

            t = tw2dict(header, tw)
            publish(channel, t)
            sleep(interval)
        #end for
    #end open


def publish(channel, tw):
    """
    Recebe um channel de MQ e um dicionario contendo as informações do tweet,
    retira somente os valores importantes e publica na fila de mensagens para o classificador
    """
    # user = literal_eval(tw["tweet_user"])
   
    body = {
        "tweet": tw['text'],
        "at": tw['name'],
        # "tweet": tw['tweet_full_text'],
        # "author": user["name"],
        # "at": user['screen_name']
    }

    channel.basic_publish(exchange='', routing_key='raw-tweets', body=dumps(body))
    print(f'tweet by @{body["at"]} published')
#end publish


def main():
    # cria a conexão com o RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', '5672'))
    print('connection started')

    # declara a fila
    channel = connection.channel()
    channel.queue_declare(queue='raw-tweets')
    print('raw-tweets queue started')

    # envia os tweets para a fila
    try:
        publishFromCSV('tweet_data.csv', channel, .5)
    finally:
        print('connection closed')
        connection.close()


if __name__ == '__main__':
    main()
"""
Este código implementa a parte Classificador de um programa de fila de mensagens que coleta,
classifica e distribui tweets de acordo com tópicos selecionados pelo cliente.

Autores:
  - Caio Miglioli @caiomiglioli
  - Ryan Lazaretti @ryanramos01

Data de Criação: 30 de Maio de 2023
Ultima alteração: 31 de Maio de 2023
"""

import pika
import json
import spacy
import time

class Classifier:
    def __init__(self):
        #colector
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', '5672'))
        self.colector = self.connection.channel()
        self.colector.queue_declare(queue='raw-tweets')

        #clients
        self.clients = self.connection.channel()

        self.clients.exchange_declare(exchange='classified-tweets', exchange_type='topic')
        self.clients.queue_declare(queue='culture')
        self.clients.queue_declare(queue='sports')
        self.clients.queue_declare(queue='news')
        self.clients.queue_declare(queue='tech')

        #keywords
        self.keywords = {
            'culture': ['music', 'artist', 'song', 'movie', 'cinema', 'critics', 'oscar', 'bafta', 'play', 'listen', 'miss', 'food', 'artistoftheyear', 'spectre', 'album', 'tv', 'tvs', 'songs', 'movies', 'abc', 'photo','season', 'review', 'performing', 'scene', 'series', 'rapper', 'show', 'drama', 'gig', 'star', 'dj', 'actors', 'actor', 'actress', 'singer', 'songwriter', 'act', 'rappers', 'book', 'gallery', 'mixtape', 'awards'],
            'sports': ['nfl', 'nba', 'mls', 'yards', 'points', 'goals','goal', 'football', 'voleyball', 'basketball', 'win', 'tennis', 'games', 'match', 'team', 'season', 'stats', 'playing', 'racing', 'game', 'plays', 'soccer', 'golf', 'drafted', 'draft', 'training', 'coach', 'defense', 'attack'],
            'news': ['video', 'politics', 'president', 'weather', 'channel', 'updates', 'watch', 'school', 'money', 'business', 'build', 'dead', 'cancer', 'latest', 'media', 'american', 'debates', 'debate', 'nation', 'democrat', 'republican', 'arrested', 'suspicion', 'economics', 'health', 'huffington', 'suspect', 'stabbing', 'economy', 'dollar', 'arrested', 'threatened', 'shoot', 'election', 'news', 'custody', 'police', 'minister'],
            'tech': ['iphone', 'samsung', 'android', 'windows', 'ios', 'bluetooth', 'wifi', 'amazon', 'videogame', 'playstation', 'xbox', 'pc', 'future', 'space','playing', 'app', 'facebook', 'game', 'processor', 'quad', 'review', 'gpu', 'cpu', '3d', 'phone', 'mobile', 'site', 'web', 'net', 'science', 'scientist', 'scientists', 'computer']
        }

        #extra
        self.nlp = spacy.load("en_core_web_sm")
    #end init


    def start(self):
        """
        Comando que inicia o servidor.
        Consome da fila 'raw-tweets' que é gerada pelo coletor, e chama a função callback 'self.classify'
        """
        self.colector.basic_consume('raw-tweets', self.classify, auto_ack=True) ### se usar auto_ack=true nao precisa do ack dentro do classify
        self.colector.start_consuming()


    def classify(self, ch, method_frame, header_frame, body):
        """
        Função que classifica os tweets recebidos e envia para os clientes a depender da fila
        """
        tweet = json.loads(body)

        #separa cada palavra em token pra comparar com as keywords
        #utiliza o nlp (spicy) para retirar as palavras como 'the, of, to, etc...'
        tokens = []
        for token in self.nlp(tweet['tweet'].lower()):
            if not token.is_stop:
                tokens.append(token.text)

        #conta a quantidade de keywords em cada topico
        tokens_counter = dict()
        tokens_found = 0

        for word in self.keywords.keys():
            for token in tokens:
                if token in self.keywords[word]:
                    if not tokens_counter.get(word):
                        tokens_counter[word] = 0
                    #conta quantas palavras o tweet tem em comum com cada topico (comparando as keywords pre estabelecidas)
                    tokens_counter[word] += 1
                    tokens_found += 1

        #se nao tiver keyword, entao abandona
        if tokens_found == 0:
            return print('NO TOPIC: ' + tweet['tweet'])
        
        #classifica (verifica com qual topico o tweet tem mais palavras em comum)
        max, topic = 0, None
        for key, value in tokens_counter.items():
            if value > max:
                topic = key

        #send
        tweet['date'] = time.time()
        self.clients.basic_publish(exchange='classified-tweets', routing_key=topic, body=json.dumps(tweet))
        # print(topic.upper() + ': ' + tweet['tweet'] + '\n')
    #end classify
#end class

if __name__ == '__main__':
    server = Classifier()
    server.start()
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
        self.clients.queue_declare(queue='culture')
        self.clients.queue_declare(queue='sports')
        self.clients.queue_declare(queue='news')
        self.clients.queue_declare(queue='tech')

        #keywords
        self.keywords = {
            'culture': ['music', 'gala', 'artist', 'song', 'movie', 'cinema', 'critics', 'oscar', 'bafta', 'play', 'listen', 'miss', 'food', 'artistoftheyear', 'spectre', 'album', 'tv', 'tvs', 'songs', 'movies', 'abc', 'season', 'series'],
            'sports': ['nfl', 'nba', 'yards', 'points', 'goals','goal', 'football', 'voleyball', 'basketball', 'win', 'tennis', 'games', 'match', 'team', 'season', 'stats', 'playing', 'racing'],
            'news': ['video', 'politics', 'president', 'weather', 'channel', 'updates', 'watch', 'school', 'money', 'business', 'build', 'dead', 'cancer', 'latest', 'media', 'american', 'debates', 'debate', 'nation', 'democrat', 'republican'],
            'tech': ['iphone', 'samsung', 'android', 'windows', 'ios', 'bluetooth', 'wifi', 'amazon', 'videogame', 'playstation', 'xbox', 'pc', 'future', 'space','playing', 'app', 'facebook']
        }

        #extra
        self.nlp = spacy.load("en_core_web_sm")
    #end init


    def start(self):
        self.colector.basic_consume('raw-tweets', self.classify, auto_ack=True) ### se usar auto_ack=true nao precisa do ack dentro do classify
        self.colector.start_consuming()


    def classify(self, ch, method_frame, header_frame, body):
        tweet = json.loads(body)

        #pega os tokens pra comparar com as keywords
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
                    tokens_counter[word] += 1
                    tokens_found += 1

        #se nao tiver keyword, entao abandona
        if tokens_found == 0:
            return print('NO TOPIC: ' + tweet['tweet'])
        
        #classifica
        max, topic = 0, None
        for key, value in tokens_counter.items():
            if value > max:
                topic = key

        #send
        tweet['date'] = time.time()
        print(tweet['date'])
        self.clients.basic_publish(exchange='', routing_key=topic, body=json.dumps(tweet))
        # print(topic.upper() + ': ' + tweet['tweet'] + '\n')
    #end classify
#end class

if __name__ == '__main__':
    server = Classifier()
    server.start()
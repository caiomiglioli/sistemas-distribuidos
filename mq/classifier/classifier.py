import pika
import json

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


    def start(self):
        self.colector.basic_consume('raw-tweets', self.classify, auto_ack=True) ### se usar auto_ack=true nao precisa do ack dentro do classify
        self.colector.start_consuming()


    def classify(self, ch, method_frame, header_frame, body):
        tweet = json.loads(body)
        print(tweet)
        #tweet['tweet']
        #tweet['author']
        #tweet['at']

        # # ack dentro do classify
        # channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    #end classify

#end class

if __name__ == '__main__':
    server = Classifier()
    server.start()
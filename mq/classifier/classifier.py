import pika
import json


#transformar tudo em classe pq vou precisar de varios channels diferentes

def classify(ch, method_frame, header_frame, body):
    tweet = json.loads(body)
    #tweet['tweet']
    #tweet['author']
    #tweet['at']


    # channel.basic_ack(delivery_tag=method_frame.delivery_tag) # ack
#end classify


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='raw-tweets')
    channel.basic_consume('raw-tweets', classify, auto_ack=True) #se usar auto_ack=true nao precisa do ack
    channel.start_consuming()
    print(' [*] Waiting for messages. To exit press CTRL+C')

if __name__ == '__main__':
    main()
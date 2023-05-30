import pika
from json import dumps
from csv import reader
from ast import literal_eval
from time import sleep

def tw2dict(header, tw):
    res = dict()
    for i, head in enumerate(header):
        res[head] = tw[i]
    return res


def publishFromCSV(filename, channel, interval):
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
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', '5672'))
    print('connection started')
    channel = connection.channel()
    channel.queue_declare(queue='raw-tweets')
    print('raw-tweets queue started')

    try:
        publishFromCSV('tweet_data.csv', channel, 1)
    finally:
        print('connection closed')
        connection.close()


if __name__ == '__main__':
    main()
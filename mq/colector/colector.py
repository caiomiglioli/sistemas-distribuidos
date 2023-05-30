import pika
import json
import csv
import ast

def tw2dict(header, tw):
    res = dict()
    for i, head in enumerate(header):
        res[head] = tw[i]
    return res


def publishFromCSV(filename, channel):
    with open(filename, newline='') as tws:
        reader = csv.reader(tws)
        header = None

        for i, tw in enumerate(reader):
            if i > 1: break
            
            if i == 0:
                header = tw
                continue

            t = tw2dict(header, tw)
            publish(channel, t)
        #end for
    #end open


def publish(channel, tw):
    user = ast.literal_eval(tw["tweet_user"])

    body = {
        "tweet": tw['tweet_full_text'],
        "author": user["name"],
        "at": user['screen_name']
    }
    
    channel.basic_publish(exchange='', routing_key='raw-tweets', body=json.dumps(body))
#end publish


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='raw-tweets')
        
    try:
        publishFromCSV('tweets.csv', channel)
    finally:
        connection.close()


if __name__ == '__main__':
    main()
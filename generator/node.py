from random import random

import json
import pika

def load():
    # generate a list of maps
    metrics = ['availableBlocks', 'freeInodes', 'availableInodes', 'freeBlocks', 'blockSize', 'totoalInodes', 'totalBlocks']

    dlist = [{
            'host': 'myhost.foobar.com',
            'service': m,
            'tags': ["sla|running"],
            'metric': random(),
        } for m in metrics]

    # send a list of maps
    for m in dlist:
        send(json.dumps(m))
    # return dlist

def send(message):
    # establish connection message with RMQ server, and send message
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    channel.basic_publish(exchange='logs', routing_key='', body=message)
    print(" [x] Sent %r" % message)
    connection.close()

if __name__ == '__main__':
    load()


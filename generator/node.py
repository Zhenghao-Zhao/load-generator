from random import random
import time, threading


import json
import pika

def load():
    # generate a list of maps and send to riemann

    metrics = ['availableBlocks', 'freeInodes', 'availableInodes', 'freeBlocks', 'blockSize', 'totoalInodes', 'totalBlocks']
    map_list = [{
            'host': 'myhost.foobar.com',
            'service': m,
            'tags': ["sla|running"],
            'metric': random(),
        } for m in metrics]

    # send a list of maps
    # todo: send those maps concurrently to established channels
    for m in map_list:
        # convert a map to string and send through
        send(json.dumps(m))

    threading.Timer(20, load).start()


def send(message):
    # establish connection with RMQ server, and send the message
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    channel.basic_publish(exchange='logs', routing_key='', body=message)
    print(" [x] Sent %r" % message)
    connection.close()

if __name__ == '__main__':
    load()


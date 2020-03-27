from random import random
import json
import pika


def load():
    """generate a list of maps and send it to riemann"""
    # establish connection with rmq
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()

    metrics = ['availableBlocks', 'freeInodes', 'availableInodes', 'freeBlocks', 'blockSize', 'totoalInodes',
               'totalBlocks']
    map_list = [
        {
            'host': 'myhost.foobar.com',
            'service': m,
            'tags': ["sla|running"],
            'metric': random(),
        } for m in metrics
    ]

    # send a list of maps
    send(map_list, channel)
    connection.close()

def send(map_list, channel):
    """establish connection with RMQ server, and send the message"""

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    for message in map_list:
        channel.basic_publish(exchange='logs', routing_key='', body=json.dumps(message))
        print(" [x] Sent %r" % message)

if __name__ == '__main__':
    print("Please start from main script")
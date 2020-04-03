"""
This class separates rmq client from load generator itself,
making the sub-systems more modular and easier to debug.

This class creates a rabbitmq client from given config and credentials,
it has send method which takes load and send to rmq server
"""

import json

import pika
import snappy


class RMQClient:

    def __init__(self, config):
        self.host = config['rmq']['host']
        self.port = config['rmq']['port']
        self.credential = pika.PlainCredentials(username=config['rmq']['username'],
                                                password=config['rmq']['password'])
        self.properties = pika.BasicProperties(content_type='application/protobuf; proto=com.aphyr.riemann.Msg')

    def send(self, load):
        """establish connection with RMQ server, compress with snappy and send the message"""

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host,
                                      port=self.port,
                                      credentials=self.credential))
        channel = connection.channel()
        channel.exchange_declare(exchange='logs', exchange_type='fanout')

        for message in load:
            message = snappy.compress(json.dumps(message))
            channel.basic_publish(exchange='logs', routing_key='', body=message, properties=self.properties)
            print(" [x] Sent %r" % message)

        connection.close()

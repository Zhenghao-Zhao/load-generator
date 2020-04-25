"""
This class separates rmq client from load generator itself,
making the sub-systems more modular and easier to debug.

This class creates a customized rabbitmq client from given config and credentials,
it has send method which takes load and send to rmq server
"""

import pika
import snappy

# some params and their default values for creating a Pika connection
PORT = 5672
USERNAME = 'guest'
PASSWORD = 'guest'
HOSTNAME = 'localhost'
VIRTUAL_HOST = '/'

class RMQClient:

    def __init__(self, config):
        self.host = config['rmq'].get('host', HOSTNAME)
        self.port = config['rmq'].get('port', PORT)
        self.vhost = config['rmq'].get('vhost', VIRTUAL_HOST)
        self.credential = pika.PlainCredentials(username=config['rmq'].get('username', USERNAME),
                                                password=config['rmq'].get('password', PASSWORD))
        self.properties = pika.BasicProperties(content_type='application/protobuf; proto=com.aphyr.riemann.Msg',
                                               content_encoding="snappy")


    def send(self, msg):
        """establish connection with RMQ server, compress with snappy and send the message"""

        # Pika requires a Pika connection per thread: https://pika.readthedocs.io/en/stable/faq.html
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host,
                                      port=self.port,
                                      virtual_host= self.vhost,
                                      credentials=self.credential))
        channel = connection.channel()
        channel.exchange_declare(exchange='logs', exchange_type='fanout')

        message = snappy.compress(msg.SerializeToString())
        channel.basic_publish(exchange='logs', routing_key='', body=message, properties=self.properties)
        print(" [x] Sent %r" % message)

        connection.close()

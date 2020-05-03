"""
This class separates rmq client from load generator itself,
making the sub-systems more modular and easier to debug.

This class creates a customized rabbitmq client from given config and credentials,
it has send method which takes load and send to rmq server
"""
import warnings

import pika
import snappy

# some params and their default values for creating a Pika connection
DEFAULT_PORT = 5672
DEFAULT_USERNAME = 'guest'
DEFAULT_PASSWORD = 'guest'
DEFAULT_HOSTNAME = 'localhost'
DEFAULT_VIRTUAL_HOST = '/'
DEFAULT_EXCHANGE_NAME = 'logs'


class RMQClient:

    def __init__(self, section):
        self.section = section
        self.host = self.__read_val('host', DEFAULT_HOSTNAME)
        self.port = self.__read_val('port', DEFAULT_PORT)
        self.vhost = self.__read_val('vhost', DEFAULT_VIRTUAL_HOST)
        self.exchange_name = self.__read_val('exchange', DEFAULT_EXCHANGE_NAME)
        self.credential = pika.PlainCredentials(username=self.__read_val('username', DEFAULT_USERNAME),
                                                password=self.__read_val('password', DEFAULT_PASSWORD))
        self.properties = pika.BasicProperties(content_type='application/protobuf; proto=com.aphyr.riemann.Msg',
                                               content_encoding="snappy")

    def __read_val(self, key, default):
        """read value from config section, return a warning and use default if no given key exists in the config file"""

        val = self.section.get(key)
        if val is None:
            message = "Key not found: " + key + '\n' + "Using default value: " + default
            warnings.warn(message)
            return default
        return val

    def batch(self, msg):
        """add incoming message to the batch"""
        return 0

    def send(self, msg):
        """establish connection with RMQ server, compress with snappy and send the message"""

        # Pika requires a Pika connection per thread: https://pika.readthedocs.io/en/stable/faq.html
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host,
                                      port=self.port,
                                      virtual_host=self.vhost,
                                      credentials=self.credential))
        channel = connection.channel()
        channel.exchange_declare(exchange=self.exchange_name, exchange_type='fanout')

        message = snappy.compress(msg.SerializeToString())
        channel.basic_publish(exchange=self.exchange_name, routing_key='', body=message, properties=self.properties)
        print(" [x] Sent %r" % message)

        connection.close()

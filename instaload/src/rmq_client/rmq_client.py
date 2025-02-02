"""
This class separates rmq client from load generator itself,
making the sub-systems more modular and easier to debug.

This class creates a customized rabbitmq client from given config and credentials,
it has send method which takes load and send to rmq server
"""
import warnings

import pika
import snappy
from .protos_out import proto_pb2

# some params and their default values for creating a Pika connection
DEFAULT_PORT = pika.ConnectionParameters.DEFAULT_PORT
DEFAULT_USERNAME = pika.ConnectionParameters.DEFAULT_USERNAME
DEFAULT_PASSWORD = pika.ConnectionParameters.DEFAULT_PASSWORD
DEFAULT_HOSTNAME = pika.ConnectionParameters.DEFAULT_HOST
DEFAULT_VIRTUAL_HOST = pika.ConnectionParameters.DEFAULT_VIRTUAL_HOST
DEFAULT_EXCHANGE_NAME = 'logs'


class RMQClient:

    def __init__(self, config):
        self.config = config
        self.host = self.__read_val('host', DEFAULT_HOSTNAME)
        self.port = self.__read_val('port', DEFAULT_PORT)
        self.vhost = self.__read_val('vhost', DEFAULT_VIRTUAL_HOST)
        self.exchange_name = self.__read_val('exchange_name', DEFAULT_EXCHANGE_NAME)
        self.credential = pika.PlainCredentials(username=self.__read_val('username', DEFAULT_USERNAME),
                                                password=self.__read_val('password', DEFAULT_PASSWORD))
        self.properties = pika.BasicProperties(content_type='application/protobuf; proto=com.aphyr.riemann.Msg',
                                               content_encoding="snappy")

    @staticmethod
    def proto_load(metrics):
        """convert metrics (dict) into proto form"""

        # generate msg with load
        msg = proto_pb2.Msg()
        for key, value in metrics.items():
            event = msg.events.add()
            event.host = 'myhost.foobar.com'
            event.service = key
            event.tags.extend(["sla|running"])
            event.metric_f = value
        return msg

    def __read_val(self, key, default):
        """read value from config section, return a warning and use default if no given key exists in the config file"""

        val = self.config[key]
        if val is None:
            message = "Key not found: " + key + '\n' + "Using default value: " + default
            warnings.warn(message)
            return default
        return val

    def send(self, metrics):
        """establish connection with RMQ server, compress with snappy and send the message"""

        msg = self.proto_load(metrics)

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

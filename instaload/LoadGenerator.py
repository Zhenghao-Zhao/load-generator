import json
import sched
import threading
import time
import pika

from random import random


class LoadGenerator:

    def __init__(self, metrics, config, node_num=1):
        """setup configs and messages"""
        self.config = config
        self.metrics = metrics
        self.node_num = node_num

    def run(self):

        # Create multiple threads that add load thread every 20s
        for i in range(self.node_num):
            threading.Thread(target=self.__add_load).start()

    def __add_load(self):
        """add load thread every 20s"""

        # Fire a thread immediately for the first time
        self.__start_load()

        s = sched.scheduler(time.time, time.sleep)
        while True:
            s.enter(20, 1, self.__start_load)
            s.run()

    def __start_load(self):
        """start a load thread"""

        # generate load
        load = self.__gen_load()

        try:
            threading.Thread(target=self.__send, args=(load,)).start()
        except:
            print("Error: unable to start thread")

    def __gen_load(self):
        """generate a list of maps and send it to riemann"""

        map_list = [
            {
                'host': 'myhost.foobar.com',
                'service': m,
                'tags': ["sla|running"],
                'metric': random(),
            } for m in self.metrics
        ]

        return map_list

    def __send(self, load):
        """establish connection with RMQ server, and send the message"""

        credential = pika.PlainCredentials(username=self.config['rmq']['username'],
                                           password=self.config['rmq']['password'])

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.config['rmq']['host'],
                                      port=self.config['rmq']['port'],
                                      credentials=credential))
        channel = connection.channel()

        channel.exchange_declare(exchange='logs', exchange_type='fanout')

        for message in load:
            channel.basic_publish(exchange='logs', routing_key='', body=json.dumps(message))
            print(" [x] Sent %r" % message)

        connection.close()

"""
The purpose of this file is to load data from external files, and pass
them to respective class/method calls
"""

import configparser
from src.load_generator import LoadGenerator
from src.rmq_client import RMQClient

if __name__ == '__main__':

    # read metrics data
    metrics = ['availableBlocks', 'freeInodes', 'availableInodes', 'freeBlocks', 'blockSize', 'totoalInodes',
               'totalBlocks']

    # read config data
    config = configparser.ConfigParser()
    config.read('data/configs/rmq.cfg')

    # create custom RMQ client
    client = RMQClient(config)

    # create a LoadGenerator that generates and sends data to a custom RMQ client
    LoadGenerator(metrics=metrics, client=client, node_num=1).run()
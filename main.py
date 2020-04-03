"""
The purpose of this file is to load data from external files, and pass
them to respective class/method calls
"""

import configparser
from instaload.LoadGenerator import LoadGenerator
from instaload.RMQClient import RMQClient

if __name__ == '__main__':

    # read metrics data
    metrics = ['availableBlocks', 'freeInodes', 'availableInodes', 'freeBlocks', 'blockSize', 'totoalInodes',
               'totalBlocks']

    # read config data
    config = configparser.ConfigParser()
    config.read('data/configs/config.cfg')

    LoadGenerator(metrics=metrics, client=RMQClient(config)).run()
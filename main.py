import configparser
from instaload.LoadGenerator import LoadGenerator

if __name__ == '__main__':

    # read metrics data
    metrics = ['availableBlocks', 'freeInodes', 'availableInodes', 'freeBlocks', 'blockSize', 'totoalInodes',
               'totalBlocks']

    # read config data
    config = configparser.ConfigParser()
    config.read('data/configs/config.cfg')

    LoadGenerator(metrics=metrics, config=config).run()
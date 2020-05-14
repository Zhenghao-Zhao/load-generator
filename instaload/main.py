"""
The purpose of this file is to load data from external files, and pass
them to respective class/method calls
"""

import configparser
import json
import threading
import argparse

from src.load_poster import LoadPoster
from src.rmq_client import RMQClient
from src.load.load import Cluster


def get_args():
    """create argparser and get arguments from cmd."""

    parser = argparse.ArgumentParser(prog='main')
    parser.add_argument('--input_config_file', default='data/configs/rmq.cfg',
                        help='Path to the input .cfg file that configures rabbitMQ')
    parser.add_argument('--input_json_file', default='data/metrics/nodes.json',
                        help='Path to the input json file that describes the format of the load you want to generate')
    args = parser.parse_args()

    return vars(args)


if __name__ == '__main__':

    path_dict = get_args()
    config_path = path_dict['input_config_file']
    json_path = path_dict['input_json_file']

    # read config data
    config = configparser.ConfigParser()
    config.read(config_path)
    # select config section to be used for connection
    section = config['rmq']
    # create custom RMQ client
    client = RMQClient(section)

    f = open(json_path)
    data = json.load(f)

    loadposter = LoadPoster(client=client)
    for c_template in data['clusters']:
        cluster = Cluster(c_template)
        # create a LoadPoster that converts load into a proper format and send via a rmq client
        threading.Thread(target=loadposter.post, args=(cluster,)).start()

"""
The purpose of this file is to load data from external files, and pass
them to respective class/method calls
"""

import json
import threading
import argparse

from src.load_dispatcher import LoadDispatcher
from src.rmq_client import RMQClient
from src.load.load import Cluster


def get_args():
    """create argparser and get arguments from cmd."""

    parser = argparse.ArgumentParser(prog='main')
    parser.add_argument('--input_config_file', default='data/configs/rabbitmq_config.json',
                        help='Path to the input json file that configures rabbitMQ')
    parser.add_argument('--input_json_file', default='data/configs/load_config.json',
                        help='Path to the input json file that describes the format of the load you want to generate')
    args = parser.parse_args()

    return vars(args)


if __name__ == '__main__':

    path_dict = get_args()
    config_path = path_dict['input_config_file']
    json_path = path_dict['input_json_file']

    f = open(config_path)
    rmq_config = json.load(f)
    # create custom RMQ client
    client = RMQClient(rmq_config)

    f = open(json_path)
    data = json.load(f)

    dispatcher = LoadDispatcher(client=client)
    for c_template in data['clusters']:
        cluster = Cluster(c_template)
        # create a LoadPoster that converts load into a proper format and send via a rmq client
        threading.Thread(target=dispatcher.dispatch, args=(cluster,)).start()

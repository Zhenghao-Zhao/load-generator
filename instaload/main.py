import json
import threading
import argparse
from src.rmq_client.rmq_client import RMQClient
from src.load.load import Cluster


def get_args():
    """
    Create argparser and get arguments from cmd.
    If nothing is passed in cmd, the default config paths are used instead.
    :return dict of config paths.
    """

    parser = argparse.ArgumentParser(prog='main')
    parser.add_argument('--input_rmq_config', default='configs/examples/rabbitmq_config.json',
                        help='Path to the input json file that configures rabbitMQ')
    parser.add_argument('--input_load_config', default='configs/examples/load_config.json',
                        help='Path to the input json file that describes the format of the load you want to generate')
    args = parser.parse_args()
    return vars(args)


if __name__ == '__main__':
    # get config paths from cmd
    path_dict = get_args()
    rmq_config_path = path_dict['input_rmq_config']
    load_config_path = path_dict['input_load_config']

    f = open(rmq_config_path)
    rmq_config = json.load(f)
    # create a RMQ client with specified connection parameters
    client = RMQClient(rmq_config)

    f = open(load_config_path)
    data = json.load(f)

    # start a thread for each cluster in the config
    for c_template in data['clusters']:
        cluster = Cluster(c_template, client)
        threading.Thread(target=cluster.dispatch_load).start()

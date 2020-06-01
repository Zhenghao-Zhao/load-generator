import sched
import threading
import time
from .metric_struct import IncMetricStruct
from .metric_struct import RandMetricStruct


class Node:
    """
    This class is responsible for generating the load of a node per call.
    """

    def __init__(self, metrics, schema, table, nid):
        """
        construct a node object.
        :param metrics: a dict of metrics from load config json file.
        :param schema: the schema number in int.
        :param table: the table number in int.
        :param nid: the id for this node.
        """

        self.id = nid
        self.metrics = metrics
        self.schema = schema
        self.table = table
        self.batch_size = 20
        self.__init_metrics()

    def __init_metrics(self):
        """
        This method first generates data into lists of batches. Each batch has size of batch_size unless it's the last
        batch.

        E.g. if when batch_size = 20: it converts
        {"metric_name_1": value, ... , "metric_name_25": value}
        to
        [{"metric_name_1": value, ... , "metric_name_20": value},
        {"metric_name_21": value, ... , "metric_name_25": value}]

        Then it stores each batch list in a MetricStruct object based on the value pattern. MetricStruct objects
        are used to update and manage the batch list for a metric.

        The MetricStruct objects are mapped to the metric variable in the argument.
        E.g. {"metric_1": MetricStruct_obj_1}
        """

        batch = {}
        # split data into batches of size batch_size or less
        for metric_name, metric_pattern in self.metrics.items():
            # get the batch list for that metric
            batch_list = []
            for s in range(1, self.schema + 1):
                for t in range(1, self.table + 1):
                    k = '/metrics/type=IndexTable/keyspace={}/scope={}/name={}/mean'.format(s, t, metric_name)
                    # from Python 3.6 onwards, the standard dict type maintains insertion order by default
                    batch[k] = 0
                    # if the batch has batch_size items or at the end of iteration,
                    # append the batch to list of that metric and create a new empty batch
                    if len(batch) == self.batch_size or (s == self.schema and t == self.table):
                        batch_list.append(batch)
                        batch = {}

            # parse metric patterns
            l = metric_pattern.split()
            if l[0] == '(>':
                self.metrics[metric_name] = IncMetricStruct(float(int(l[1])), float(l[2][1:]), float(l[4][:-2]),
                                                            batch_list)
            else:
                self.metrics[metric_name] = RandMetricStruct(float(l[0][1:]), float(l[-1][:-1]), batch_list)

    def get_next_batch(self):
        """
        Get the next batch (a dict) off each metric struct and combine them into a single dict.
        """

        metrics = {}
        for struct in self.metrics.values():
            metrics = {**metrics, **struct.get_next_batch()}

        return metrics


class Cluster:
    """
    This class manages the communication between a node and a rmq client.
    The communication can only exist through a cluster.
    """

    def __init__(self, c_config, client):
        """
        Construct a cluster object.
        :param c_config: a dict with property specification for a cluster.
        :param client: a rabbitMQ client as a rmq_client object.
        """
        self.id = c_config['id']
        self.nodes = []
        self.client = client
        self.period = 20
        self.__init_load(c_config)

    def __init_load(self, c_config):
        """
        Initialize nodes according to the given cluster config.
        """

        n_config = c_config['nodes']
        lst = []
        for n in n_config:
            node_num = n['count']
            # generate a number of nodes with the same config according to "count" property
            for i in range(node_num):
                node = Node({**c_config['metrics'], **n['additional_metrics']}, c_config['schema'],
                            c_config['table'], n['id'])
                lst.append(node)
        self.nodes = lst

    def dispatch_load(self):
        """
        Start a thread for each node in the cluster that dispatches the load generated through a node.
        """

        for node in self.nodes:
            threading.Thread(target=self.__start_load, args=(node,)).start()

    def __start_load(self, node):
        """
        Start a python scheduler that runs periodically according to self.period. When running, the scheduler starts a
        new thread that get the load from the node and calls the method that sends the load.
        """

        # fire a thread immediately for the first time
        self.__send_load(node.get_next_batch())

        s = sched.scheduler(time.time, time.sleep)
        while True:
            s.enter(self.period, 1, self.__send_load, argument=(node.get_next_batch(),))
            s.run()

    def __send_load(self, metrics):
        """
        Start a thread that calls the client's send method to send the metrics down the pipeline.
        """

        try:
            threading.Thread(target=self.client.send, args=(metrics,)).start()
        except:
            print("Error: unable to start thread")

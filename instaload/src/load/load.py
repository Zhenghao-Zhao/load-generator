from .metric_struct import IncMetricStruct
from .metric_struct import RandMetricStruct


class Node:
    """the load generated by a node"""

    def __init__(self, metrics, schema, table, n_template):
        """takes in a dict of metrics, with metric value range as value"""

        self.metrics = metrics
        self.schema = schema
        self.table = table
        self.id = n_template['id']
        self.batch_size = 20
        self.__init_metrics()

    def __init_metrics(self):
        """initialize metrics"""

        # parsing metric patterns
        for metric_name, metric_pattern in self.metrics.items():
            l = metric_pattern.split()
            if l[0] == '(>':
                self.metrics[metric_name] = IncMetricStruct(float(l[2][1:]), float(l[4][:-2]))
            else:
                self.metrics[metric_name] = RandMetricStruct(float(l[0][1:]), float(l[-1][:-1]))

        # initialize a batch: a dict of size 20
        mini_batch = {}
        for key, struct in self.metrics.items():
            batch_list = []
            for s in range(1, self.schema + 1):
                for t in range(1, self.table + 1):
                    k = '/metrics/type=IndexTable/keyspace={}/scope={}/name={}/mean'.format(s, t, key)
                    # From Python 3.6 onwards, the standard dict type maintains insertion order by default.
                    mini_batch[k] = 0
                    # if the batch has 20 items or at the end of iteration,
                    # append the batch to list of that metric and create a new empty batch
                    if len(mini_batch) == self.batch_size or (s == self.schema and t == self.table):
                        batch_list.append(mini_batch)
                        mini_batch = {}

            struct.set_batch_list(batch_list)

    def get_next_batch(self):
        """get the next batch (a dict) off each metric struct and combine them into single dict"""

        rst = {}
        for struct in self.metrics.values():
            rst = {**rst, **struct.get_next_batch()}

        return rst


class Cluster:
    """a collection of loads generated by a number of nodes"""

    def __init__(self, c_template):
        self.id = c_template['id']
        self.cluster_number = c_template['count']

        self.node_number = 0
        self.nodes = []
        self.__init_load(c_template)

    def __init_load(self, c_template):
        """initialize node load"""

        node_templates = c_template['nodes']
        lst = []
        for c in range(self.cluster_number):
            for n in node_templates:
                node_num = n['count']
                for i in range(node_num):
                    node = Node({**c_template['metrics'], **n['additional_metrics']}, c_template['schema'],
                                c_template['table'], n)
                    # amoritized 0(1)
                    lst.append(node)

        self.node_number = len(lst)
        self.nodes = lst

    def get_node(self, nid):
        """retrieve a node object from the list"""

        return self.nodes[nid]

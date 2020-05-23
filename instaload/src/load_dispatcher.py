"""
This class separates rmq client from load generator itself,
making the sub-systems more modular and easier to debug.

This class generates load and makes call to rmq client send method to send data down the pipeline
"""

import sched
import threading
import time
from .protos_out import proto_pb2


class LoadDispatcher:

    def __init__(self, client):
        self.client = client
        self.period = 10

    def dispatch(self, cluster):

        # Create multiple scheduler threads that add a load thread every 20s
        for i in range(cluster.node_number):
            node = cluster.get_node(i)
            threading.Thread(target=self.__add_load, args=(node,)).start()

    def __add_load(self, node):
        """run a python scheduler periodically. The scheduler starts a new thread that generates and sends load"""

        # Fire a thread immediately for the first time
        self.__send_load(node.get_next_batch())

        s = sched.scheduler(time.time, time.sleep)
        while True:
            s.enter(self.period, 1, self.__send_load, argument=(node.get_next_batch(),))
            s.run()

    def __send_load(self, metrics):
        """start a load thread"""

        # generate msg with load
        msg = self.__gen_msg(metrics)

        # send load
        try:
            threading.Thread(target=self.client.send, args=(msg,)).start()
        except:
            print("Error: unable to start thread")

    def __gen_msg(self, metrics):
        """generate a Msg instance that contains the metrics for a node. Msg is the format we use to send load"""

        msg = proto_pb2.Msg()

        for key, value in metrics.items():
            event = msg.events.add()
            event.host = 'myhost.foobar.com'
            event.service = key
            event.tags.extend(["sla|running"])
            event.metric_f = value

        return msg
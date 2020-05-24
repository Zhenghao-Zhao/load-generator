import random


class MetricStruct:
    """
    A metric struct object is responsible for updating and managing the passed in batch list for that metric.
    A batch list contains batches of metric data.
    Its child class should have a method for updating the metric values. See examples below.
    """

    def __init__(self, batch_list):
        self.batch_list = batch_list
        self.current_batch_index = 0

    def get_new_metric_value(self):
        return 0

    def __update_batch_list(self):
        """update the values of metrics in the batch list"""

        current_value = self.get_new_metric_value()
        for batch in self.batch_list:
            for key, value in batch.items():
                batch[key] = current_value

        self.current_batch_index = 0

    def get_next_batch(self):
        """get the batch at the current batch index"""

        rst = self.batch_list[self.current_batch_index]
        if self.current_batch_index+1 == len(self.batch_list):
            self.__update_batch_list()
        else:
            self.current_batch_index += 1

        return rst


class IncMetricStruct(MetricStruct):
    """increasing metrics"""

    def __init__(self, a, b, batch_list):
        super().__init__(batch_list)
        self.a = a
        self.b = b
        self.current = 0

    def get_new_metric_value(self):
        """generates metric values using (> a (b ~ c))"""

        self.current = self.current + random.uniform(self.a, self.b)
        return self.current


class RandMetricStruct(MetricStruct):
    """random metrics"""

    def __init__(self, a, b, batch_list):
        super().__init__(batch_list)
        self.a = a
        self.b = b

    def get_new_metric_value(self):
        """generates metric values using (a ~ b)"""

        return random.uniform(self.a, self.b)


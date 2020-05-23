import random


class MetricStruct:
    """base class for metric objects"""

    def __init__(self):
        self.batch_list = []
        self.current_batch_index = 0

    def get_new_metric_value(self):
        return 0

    def __update_batch(self):
        """update the values of metrics in the batch list"""

        current_value = self.get_new_metric_value()
        for batch in self.batch_list:
            for key, value in batch.items():
                batch[key] = current_value

        self.current_batch_index = 0

    def set_batch_list(self, batch_list):
        """replace holding batch with input batch list and update batch values"""

        self.batch_list = batch_list
        self.__update_batch()

        print(self.batch_list)

    def get_next_batch(self):
        """get the batch at the current batch index"""

        rst = self.batch_list[self.current_batch_index]
        if self.current_batch_index+1 == len(self.batch_list):
            self.__update_batch()
        else:
            self.current_batch_index += 1

        return rst


class IncMetricStruct(MetricStruct):
    """increasing metrics"""

    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b
        self.current = 0

    def get_new_metric_value(self):
        """generates metric values using (> a (b ~ c))"""

        self.current = self.current + random.uniform(self.a, self.b)
        return self.current


class RandMetricStruct(MetricStruct):
    """random metrics"""

    def __init__(self, a, b):
        super().__init__()
        self.a = a
        self.b = b

    def get_new_metric_value(self):
        """generates metric values using (a ~ b)"""

        return random.uniform(self.a, self.b)


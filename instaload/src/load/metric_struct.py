import random


class MetricStruct:
    """
    A MetricStruct object is responsible for updating and managing the batch list for a metric.
    A batch list contains batches of metric data. The metric values in that batch list are the same.
    e.g. [{"metric_name_1": value, ... , "metric_name_20": value},{"metric_name_21": value}].
    Its child classes should at least have a method for updating the metric values. See examples below.
    """

    def __init__(self, batch_list):
        """
        Construct a MetricStruct object
        :param batch_list: e.g. [{"metric_name_1": value, ... , "metric_name_20": value},{"metric_name_21": value}]
        """

        self.batch_list = batch_list
        self.next_batch_index = 0
        # update metric value for all batches
        self.__update_batch_list()

    def __update_batch_list(self):
        """
        Update the metric values in the batch.
        """

        current_value = self.get_new_metric_value()
        for batch in self.batch_list:
            for key, value in batch.items():
                batch[key] = current_value

    def get_new_metric_value(self):
        """
        How you want to update the metric value.
        """
        return 0

    def get_next_batch(self):
        """
        Get the batch at the current batch index.
        """

        if self.next_batch_index == len(self.batch_list):
            self.next_batch_index = 0
            self.__update_batch_list()

        rst = self.batch_list[self.next_batch_index]
        self.next_batch_index += 1
        return rst


class IncMetricStruct(MetricStruct):
    """
    The class extends MetricsStruct with its own method for updating the metric value.
    Updating method: (> a (b ~ c)), start with a, increase randomly between b and c at each update.
    """

    def __init__(self, a, b, c, batch_list):
        """
        Construct a IncMetricStruct object.
        :param a: value a in (> a (b ~ c)), starting value.
        :param b: value b in (> a (b ~ c)), lower limit of random increasing by value.
        :param c: value c in (> a (b ~ c)), upper limit of random increasing by value.
        :param batch_list: see super class.
        """
        self.current = a
        self.b = b
        self.c = c
        super().__init__(batch_list)

    def get_new_metric_value(self):
        """
        Generates metric values using (> a (b ~ c)).
        """

        self.current = self.current + random.uniform(self.b, self.c)
        return self.current


class RandMetricStruct(MetricStruct):
    """
    The class extends MetricsStruct with its own method for updating the metric value.
    Updating method: (a ~ b), random between given a and b.
    """

    def __init__(self, a, b, batch_list):
        """
        Construct a RandMetricStruct object.
        :param a: value a in (a ~ b), lower limit of the random value.
        :param b: value b in (a ~ b), upper limit of the random value.
        :param batch_list: see super class.
        """
        self.a = a
        self.b = b
        super().__init__(batch_list)

    def get_new_metric_value(self):
        """
        Generates metric values using (a ~ b).
        """

        return random.uniform(self.a, self.b)


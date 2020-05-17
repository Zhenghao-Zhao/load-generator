import random

class Metric:
    """base class for metric objects"""
    def __init__(self, current):
        self.current = current

    def update(self):
        return self.current


class IncMetric(Metric):
    """increasing metrics"""

    def __init__(self, current, a, b):
        super().__init__(current)
        self.a = a
        self.b = b

    def update(self):
        """generates metric values using (> a (b ~ c))"""

        self.current = self.current + random.uniform(self.a, self.b)
        return self.current


class RandMetric(Metric):
    """random metrics"""

    def __init__(self, current, a, b):
        super().__init__(current)
        self.a = a
        self.b = b

    def update(self):
        """generates metric values using (a ~ b)"""

        self.current = random.uniform(self.a, self.b)
        return self.current


class ArithmeticProgression:
    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end

    def __iter__(self):
        # Coerce beginning value to the type of subsequent additions.
        result = type(self.begin + self.step)(self.begin)
        forever = self.end is None  # Unbounded series if end is None.
        index = 0
        while forever or result < self.end:
            yield result
            index += 1
            result = self.begin + self.step * index

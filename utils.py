
import time
import numpy as np

class TimeRecord:
    def __init__(self):
        self.time_begin = None
        self.time_list = []

    def __enter__(self):
        self.time_begin = time.time()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        time_elapsed = time.time() - self.time_begin
        self.time_begin = None
        self.time_list.append(time_elapsed)

    def report(self):
        tl = self.time_list
        print(f"mean: {np.mean(tl)} std: {np.std(tl)} len: {len(tl)}")

def target_generator(f):
    def _target(in_queue, out_queue):
        while True:
            x = in_queue.get()
            # y = f(x, sleep_time)
            y = f(x)
            out_queue.put(y)
    return _target


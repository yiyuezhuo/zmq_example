
import time
import numpy as np
from contextlib import contextmanager
from typing import List
from scipy import stats
import zmq
import timeit

@contextmanager
def simulate_processing_time(fake_processing_time):
    time_begin = time.time()
    yield
    time_end = time.time()
    time_elapse = time_end - time_begin
    time_sleep = fake_processing_time - time_elapse
    # print(f"time_elapse:{time_elapse}, time_sleep:{time_sleep}")
    assert time_sleep > 0
    time.sleep(time_sleep)

"""
@contextmanager
def simulate_processing_time_acc(fake_processing_time):
    time_begin = timeit.default_timer()
    yield
    time_end = timeit.default_timer()
    time_elapse = time_end - time_begin
    time_sleep = fake_processing_time - time_elapse
    # print(f"time_elapse:{time_elapse}, time_sleep:{time_sleep}")
    assert time_sleep > 0
    time.sleep(time_sleep)
"""

def fake_video(*, frames:int, fps: int, size: tuple=(800, 600,3)):
    sleep_time = 1 / fps
    for _ in range(frames):
        with simulate_processing_time(sleep_time):
            yield (np.random.random(size) * 255).astype(np.uint8) # pylint: disable=no-member

def segmentation1(x: np.ndarray, sleep_time:float):
    with simulate_processing_time(sleep_time):
        return x * 0.75

def segmentation2(x: np.ndarray, sleep_time:float):
    with simulate_processing_time(sleep_time):
        return x * 0.25

def classification(x: np.ndarray, sleep_time:float, n_classes:int):
    #
    with simulate_processing_time(sleep_time):
        return stats.dirichlet(np.ones(n_classes)).rvs()



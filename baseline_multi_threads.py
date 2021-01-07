
from fake_processes import fake_video, segmentation1, segmentation2, classification
from utils import TimeRecord, target_generator

import queue
import numpy as np
from threading import Thread

from click import command, option


@command()
@option('--coef', default=1, type=float)
@option('--n_classes', default=4, type=int)
@option('--frames', default=250, type=int)
@option('--fps', default=25, type=int)
@option('--width', default=1920, type=int)
@option('--height', default=1080, type=int)
@option('--channels', default=3, type=int)
def main(coef, n_classes, frames, fps, width, height, channels):

    seg1_target = target_generator(lambda x: segmentation1(x, 0.03 * coef))
    seg2_target = target_generator(lambda x: segmentation2(x, 0.04 * coef))

    @target_generator
    def class_target(x):
        return classification(x, 0.05 * coef, n_classes)

    target_list = [seg1_target, seg2_target, class_target]
    queue_list = [(queue.Queue(), queue.Queue()) for target in target_list]
    thread_list = [Thread(target=target, args=qio) for target, qio in zip(target_list, queue_list)]

    for thread in thread_list:
        thread.start()

    time_recorder = TimeRecord()

    size = (height, width, channels)
    for frame in fake_video(frames=frames, fps=fps, size=size):
        with time_recorder:

            for qi, _ in queue_list:
                qi.put(frame)
            for _, qo in queue_list:
                qo.get()

    time_recorder.report()

if __name__ == '__main__':
    # This likely will work due to GIL, check multi-processes baseline.
    main() # pylint: disable=no-value-for-parameter
    # parameters will be passed in by click

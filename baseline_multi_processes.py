from fake_processes import fake_video, segmentation1, segmentation2, classification
from utils import TimeRecord, target_generator

import numpy as np
from multiprocessing import Process, Queue
#from pathos.multiprocessing import Process, Queue

from clize import run


# seg1_target = target_generator(lambda x: segmentation1(x, 0.03 * coef))
# seg2_target = target_generator(lambda x: segmentation2(x, 0.04 * coef))

g_dict = {
    "coef": 1,
    "n_classes": 4
}

@target_generator
def seg1_target(x):
    return segmentation1(x, 0.03 * g_dict["coef"])

@target_generator
def seg2_target(x):
    return segmentation2(x, 0.04 * g_dict["coef"])

@target_generator
def class_target(x):
    return classification(x, 0.05 * g_dict["coef"], g_dict["n_classes"])

def set_g_dict(coef, n_classes):
    g_dict["coef"] = coef
    g_dict["n_classes"] = n_classes


def main(*, coef=1., n_classes=4, frames=250, fps=25, width=1920, height=1080, channels=3):
    target_list = [seg1_target, seg2_target, class_target]
    queue_list = [(Queue(), Queue()) for target in target_list]
    set_g_dict(coef, n_classes)

    process_list = [Process(target=target, args=qio) for target, qio in zip(target_list, queue_list)]

    for process in process_list:
        process.start()

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
    run(main)

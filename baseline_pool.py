
# https://research.wmz.ninja/articles/2018/03/on-sharing-large-arrays-when-using-pythons-multiprocessing.html

from multiprocessing import Pool, RawArray
from fake_processes import fake_video, segmentation1, segmentation2, classification
import numpy as np
from clize import run
from utils import TimeRecord
from ctypes import c_uint8

G = {
    "frame": None,
    "output_segmentation1": None,
    "output_segmentation2": None,
    "classification": None
}

def set_G(dic):
    for key, arr_shape_dtype in dic.items():
        G[key] = unpack(*arr_shape_dtype)

def init(dic):
    print("init")
    set_G(dic)

def pack(mat):
    raw_arr = RawArray(c_uint8, mat.nbytes)
    view = np.frombuffer(raw_arr, dtype=mat.dtype).reshape(mat.shape)
    np.copyto(view, mat)
    return raw_arr, mat.shape, mat.dtype

def unpack(arr, shape, dtype):
    return np.frombuffer(arr, dtype=dtype).reshape(shape)

def do_segmentation1(sleep_time):
    output = segmentation1(G["frame"], sleep_time)
    np.copyto(G["output_segmentation1"], output) # TODO: adapt segmentation1 to use pre-allocated memory

def do_segmentation2(sleep_time):
    output = segmentation2(G["frame"], sleep_time)
    np.copyto(G["output_segmentation2"], output)

def do_classification(sleep_time, n_classes):
    output = classification(G["frame"], sleep_time, n_classes)
    np.copyto(G["output_classification"], output)


def main(*, coef=1, n_classes=4, frames=250, fps=25, 
            width=1920, height=1080, channels=3, 
            num_workers=3):
    shape = [height, width, channels]

    pre_alloc_dic = {
        "frame": pack(np.zeros(shape, dtype=np.uint8)),
        "output_segmentation1": pack(np.zeros(shape)),
        "output_segmentation2": pack(np.zeros(shape)),
        "output_classification": pack(np.zeros(n_classes))
    }

    init(pre_alloc_dic) # set G

    task_list = [
        (do_segmentation1, [coef * 0.03]),
        (do_segmentation2, [coef * 0.04]),
        (do_classification, [coef * 0.05, n_classes])
    ]

    time_recorder = TimeRecord()

    with Pool(num_workers, initializer=init, initargs=[pre_alloc_dic]) as pool:
        for frame in fake_video(frames=frames, fps=fps, size=shape):
            res_list = []
            with time_recorder:
                np.copyto(G["frame"], frame)
                for (func, args) in task_list:
                    res_list.append(pool.apply_async(func, args))
                for res in res_list:
                    res.get()
            # Now pre_alloc_dic["output_segmentation1"] etc are outputs for this phase.

    time_recorder.report()
    print(time_recorder.time_list[:5], "...", time_recorder.time_list[-5:])

#"""
if __name__ == '__main__':
    run(main)
#"""
"""
if __name__ == '__main__':
    main()
"""

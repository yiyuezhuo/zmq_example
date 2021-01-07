
from fake_processes import segmentation1, segmentation2, classification
from clize import run
import zmq

def process(frame, base_sleep_time, n_classes):
    rs1 = segmentation1(frame, base_sleep_time * 0.03)
    rs2 = segmentation2(frame, base_sleep_time * 0.04)
    rs3 = classification(frame, base_sleep_time * 0.05, n_classes)
    return rs1, rs2, rs3

def main(upstream_host, downstream_host, *, base_sleep_time=1., n_classes=4):



if __name__ == "__main__":
    run(main)
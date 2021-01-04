
import zmq
import numpy as np
from fake_processes import segmentation1, segmentation2, classification
from zmq_utils import send_array, recv_array
from pathlib import Path


class FakeServer:
    def __init__(self, server_name, sleep_time, *, 
                 addr="tcp://127.0.0.1", port=None, tmp_root="_server_ports"):
        context = zmq.Context()
        socket = context.socket(zmq.REP) # pylint: disable=no-member

        if port is not None:
            addr = addr + str(port)
            socket.bind(addr)
        else:
            port = socket.bind_to_random_port(addr)
            addr = addr + str(port)
        
        print(f"Listening to: {addr}")
        root = Path(tmp_root)
        root.mkdir(exist_ok=True)
        with open(root / server_name, "w") as f:
            f.write(str(port))

        self.socket = socket
        self.server_name = server_name
        self.sleep_time = sleep_time
        self.addr = addr

    def start(self):
        print(f"{self.server_name} at {self.addr} (sleep_time={self.sleep_time}) Started")
        while True:
            input_array = recv_array(self.socket)
            print(f"Received request {input_array.shape}")

            y = self.process(input_array)

            send_array(self.socket, y)

            #  Send reply back to client
            print(f"Sent {y.shape}")

    def process(self, x):
        raise NotImplementedError

class FakeSegmentation1(FakeServer):
    def process(self, x):
        return segmentation1(x, self.sleep_time)

class FakeSegmentation2(FakeServer):
    def process(self, x):
        return segmentation2(x, self.sleep_time)

class FakeClassification(FakeServer):
    def __init__(self, *args, n_classes, **kwargs):
        super().__init__(*args, **kwargs)
        self.n_classes = int(n_classes)

    def process(self, x):
        return classification(x, self.sleep_time, self.n_classes)


def main():
    import argparse
    parser = argparse.ArgumentParser("Fake Servers")
    parser.add_argument("start_server")
    parser.add_argument("sleep_time", type=float)
    parser.add_argument("--server_name", default=None)
    parser.add_argument("--n_classes", default=None)
    parser.add_argument("--test", action="store_true")

    args = parser.parse_args()
    print(args)
    if args.test:
        return
    if args.server_name is None:
        args.server_name = args.start_server

    cls = globals()[args.start_server] 
    cls_args = [args.server_name, args.sleep_time]
    cls_kwargs = {"n_classes": args.n_classes} if args.n_classes is not None else {}
    server = cls(*cls_args, **cls_kwargs)
    server.start()


if __name__ == '__main__':
    main()

"""
$ python fake_zmq_server.py FakeSegmentation1 0.03
$ python fake_zmq_server.py FakeSegmentation2 0.04
$ python fake_zmq_server.py FakeClassification1 0.05 --n_classes 4
"""

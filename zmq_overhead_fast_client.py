import numpy as np
import zmq
from zmq_utils import send_array_fast, recv_array_fast
import time
import argparse

parser = argparse.ArgumentParser("Overhead test CLI")
parser.add_argument("--height", type=int, default=2000)
parser.add_argument("--width", type=int, default=1000)
parser.add_argument("--channels", type=int, default=3)
parser.add_argument("--samples", type=int, default=100)
parser.add_argument("--addr", default="tcp://127.0.0.1:10000")

args = parser.parse_args()

addr = args.addr

context = zmq.Context()

server = context.socket(zmq.REQ) # pylint: disable=no-member
server.connect(addr)

img_shape = [args.height, args.width, args.channels]
x = (np.random.random(img_shape) * 255).astype(np.uint8) # fake image
print(f"{type(x)} {x.shape}")

time_begin = time.time()
for i in range(args.samples):
    send_array_fast(server, x)
    recv_array_fast(server)
time_end = time.time()
time_elapsed = time_end - time_begin

print(f"time_elapsed={time_elapsed} mean={time_elapsed / args.samples}")
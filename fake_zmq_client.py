
from zmq_utils import send_array, recv_array
from fake_processes import fake_video
from pathlib import Path
import zmq
from queue import Queue
from collections import deque
from threading import Thread
import numpy as np
import time

import argparse

parser = argparse.ArgumentParser("Fake zmq video example")
parser.add_argument("--frames", default=250, type=int)
parser.add_argument("--fps", default=25, type=int)

args = parser.parse_args()
print(args)


context = zmq.Context()

server_name_list = [
    "FakeSegmentation1",
    "FakeSegmentation2",
    "FakeClassification"
]

root = Path("_server_ports")

addr_map = {}
server_map = {}
for server_name in server_name_list:
    with open(root / server_name) as f:
        port = f.read()
        addr = "tcp://127.0.0.1:" + port
    addr_map[server_name] = addr

    server = context.socket(zmq.REQ) # pylint: disable=no-member
    server.connect(addr)
    server_map[server_name] = server

def load_thread(queue, *, frames=250, fps=25, required_len=16):
    frame_deque = deque(maxlen=required_len)
    for frame in fake_video(frames=frames, fps=fps):
        frame_deque.append(frame)
        if len(frame_deque) == required_len: # and queue.empty():
            queue.put(frame_deque)

# frame_list_queue = Queue(maxsize=1)
frame_list_queue = Queue()

t = Thread(target=load_thread, args=(frame_list_queue,),
           kwargs=dict(frames=args.frames, fps=args.fps))
t.start()

time_list = []

while True:
    if not t.is_alive() and frame_list_queue.empty():
        break

    frame_list = frame_list_queue.get()
    time_begin = time.time()

    last_frame = frame_list[-1]
    section = np.stack(frame_list)

    input_map = {
        "FakeSegmentation1": last_frame,
        "FakeSegmentation2": last_frame,
        "FakeClassification": section
    }

    for server_name, server in server_map.items():
        input_array = input_map[server_name]
        send_array(server, input_array)
        print(f"Sent to {server_name} {input_array.shape}")
    
    for server_name, server in server_map.items():
        out = recv_array(server)
        
        if len(out.shape) == 1: # classification probability vector
            print(f"Recv from {server_name}: {out}")
        else:
            print(f"Recv from {server_name}: {out.shape}")
        
    
    time_end = time.time()
    time_elapsed = time_end - time_begin

    time_list.append(time_elapsed)

print(f"mean: {np.mean(time_list)}, std: {np.std(time_list)} len: {len(time_list)}")
if len(time_list) < 100:
    print(time_list)
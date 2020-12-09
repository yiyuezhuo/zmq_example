
import time
import zmq

context = zmq.Context()

addr_list = ["tcp://localhost:10001", "tcp://localhost:10002"]

#  Socket to talk to server
print("Connecting to hello world server…")

server_list = []
for addr in addr_list:
    server = context.socket(zmq.REQ)
    server.connect(addr)
    server_list.append(server)

time_begin = time.time()

for addr, server in zip(addr_list, server_list):
    print(f"Sending request to {addr}")
    server.send(b"Hello")

    message = server.recv()
    print(f"Received reply from {addr}: {message}")

time_end = time.time()

print(f"Elapse: {time_end - time_begin}")

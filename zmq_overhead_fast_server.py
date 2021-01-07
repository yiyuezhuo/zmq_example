
from zmq_utils import send_array_fast, recv_array_fast
import zmq

addr = "tcp://127.0.0.1:10000"

context = zmq.Context()
socket = context.socket(zmq.REP) # pylint: disable=no-member
socket.bind(addr)

print(f"Listening to: {addr}")

while True:
    data = recv_array_fast(socket, copy=False)
    send_array_fast(socket, data, copy=False)

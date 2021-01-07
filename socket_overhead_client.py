
import socket
from clize import run
from socket_utils import mat, nbytes
from timeit import timeit
import numpy as np

mat_cache = np.empty_like(mat)

def send_and_recv(s: socket.socket):
    # s.sendall(memoryview(mat))
    # s.sendall(mat)
    # sr = np.frombuffer(s.recv(nbytes), dtype=np.uint8)
    # print(memoryview(sr).nbytes)
    s.sendall(mat)
    s.recv_into(mat_cache, nbytes)

def main(*, host="127.0.0.1", port=10000, number=100):

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Connecting to {host}:{port}")
        f = lambda: send_and_recv(s)
        elapsed = timeit(f, number=number)

    print(f"Second per send_and_recv: {elapsed / number}")
    return elapsed

if __name__ == "__main__":
    run(main)
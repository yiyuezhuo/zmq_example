
import socket
from socket_utils import size, nbytes, mat
from clize import run
import numpy as np

mat_cache = np.empty_like(mat)

def main(*, host="127.0.0.1", port=10000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Listening to {host}:{port}")
        while True:
            print("Wait new accept")
            conn, addr = s.accept()
            while True:
                conn.recv_into(mat_cache, nbytes)
                # a = np.frombuffer(conn.recv(nbytes), dtype=np.uint8)
                # print(memoryview(a).nbytes)
                #conn.sendall(memoryview(a))
                # conn.sendall(a)
                conn.sendall(mat_cache)
            conn.close()


if __name__ == '__main__':
    run(main)
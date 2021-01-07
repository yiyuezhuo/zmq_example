
# https://zguide.zeromq.org/docs/chapter3/#The-Load-Balancing-Pattern

from clize import run
import subprocess

def main(*, num_workers=3, base_port=10000, host="tcp://127.0.0.1"):
    for i in range(num_workers):
        port = base_port + i
        addr = f"{host}:{port}"
        


if __name__ == '__main__':
    run(main)
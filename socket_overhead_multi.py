from clize import run
from threading import Thread
import subprocess

side_map = {
    "client": "socket_overhead_client.py",
    "server": "socket_overhead_server.py"
}

def main(side:str, *, n_thread=3, host="127.0.0.1", port_base=10000, number=100):
    script = side_map[side]
    thread_list = []
    for i in range(n_thread):
        port = port_base + i
        command = ["python", script, "--host", host, "--port", str(port)]
        if side == "client":
            command += ["--number", str(number)]
        thread = Thread(target=subprocess.run, args=[command], daemon=True)
        thread_list.append(thread)
    
    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()


if __name__ == '__main__':
    run(main)
    # 6 cores -> n_thread=3, 4 cores -> n_thread=2
    # python socket_overhead_multi.py server
    # python socket_overhead_multi.py client
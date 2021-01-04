
from threading import Thread
import subprocess
import time
import argparse

parser = argparse.ArgumentParser("Fake video example launch tool")
parser.add_argument("--coef", default=1, type=float)

args = parser.parse_args()
print(args)

server_command_list = [
    ["python", "fake_zmq_servers.py", "FakeSegmentation1", str(0.03*args.coef)],
    ["python", "fake_zmq_servers.py", "FakeSegmentation2", str(0.04*args.coef)],
    ["python", "fake_zmq_servers.py", "FakeClassification", str(0.05*args.coef), "--n_classes" ,"4"]
]

t_list = []

for command in server_command_list:
    t = Thread(target=subprocess.run, args=[command], daemon=True)
    t.start()
    t_list.append(t)

# Comment following code to debug
# ipython -i fake_launch_servers.py -- --coef 1
#"""
while True:
    # use ctrl+c to exit
    time.sleep(1)
#"""


import time
import zmq

def start_server(addr, message, sleep_time=1):

    print(f"Listening to: {addr}")

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(addr)

    while True:
        #  Wait for next request from client
        message = socket.recv()
        print("Received request: %s" % message)

        #  Do some 'work'
        time.sleep(sleep_time)

        #  Send reply back to client
        socket.send(message)

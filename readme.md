
# ZMQ server parallel example

Start servers

```shell
$ python server1.py
$ python server2.py
```

test non-parallel time elapse

```shell
$ python client_non_parallel.py
```

Output:

```
Connecting to hello world server…
Sending request to tcp://localhost:10001
Received reply from tcp://localhost:10001: b'Hello'
Sending request to tcp://localhost:10002
Received reply from tcp://localhost:10002: b'Hello'
Elapse: 2.028697967529297
```

Test parallel time elapse:

```shell
$ python client_parallel.py

```

Output:

```
Connecting to hello world server…
Sending request to tcp://localhost:10001
Sending request to tcp://localhost:10002
Received reply from tcp://localhost:10001: b'Hello'
Received reply from tcp://localhost:10002: b'Hello'
Elapse: 1.0200190544128418
```
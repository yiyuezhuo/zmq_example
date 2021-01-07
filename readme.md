
# ZMQ server parallel example

## Basic

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

## Fake Video processing

This example client will take video from a fake source and send it to three servers to make them to compute at the same time. The cost is simulated by `time.sleep`, 30ms, 40ms, 50ms.

Start servers:

```shell
$ python fake_launch_servers.py
```

When all 3 servers have started:

```shell
$ python fake_zmq_client.py --frames 25
```

The output:

```
mean: 0.12734580039978027, std: 0.008269703592629206 len: 10
[0.12698078155517578, 0.12700295448303223, 0.11149859428405762, 0.12528395652770996, 0.12562036514282227, 0.12398099899291992, 0.12505340576171875, 0.12497234344482422, 0.14205336570739746, 0.14101123809814453]
```

The list just shows the elapsed time (second) for every parallel evaluate. The ideal value is 0.05, but we found mean value 0.12. The error is 0.12-0.05=0.07. 

Slow mode (x10 sleep time, [why](#Why)?)

```shell
$ python fake_launch_servers.py --coef 10
```

```shell
$ python fake_zmq_client.py --frames 25
```

The output:
```
mean: 0.5766829967498779, std: 0.01413372427198757 len: 10
[0.5643060207366943, 0.5917575359344482, 0.5610442161560059, 0.5895097255706787, 0.5598571300506592, 0.5811591148376465, 0.557636022567749, 0.5945043563842773, 0.5754392147064209, 0.5916166305541992]
```

The ideal value is 0.5, the error is 0.57-0.5=0.07.

Slower mode (x100 sleep time, [why](#Why)?)

```shell
$ python fake_launch_servers.py --coef 100
```

```shell
$ python fake_zmq_client.py --frames 25
```

The output:
```
mean: 5.067905068397522, std: 0.00904631569773037 len: 10
[5.066768407821655, 5.082828760147095, 5.061943769454956, 5.062634229660034, 5.083930969238281, 5.0588366985321045, 5.070153474807739, 5.0649683475494385, 5.071840286254883, 5.055145740509033]
```

The ideal value is 5, so the error is 5.067-5=0.067.

### why

The functions used to simulate the overhead, `simulate_processing_time` and `time.sleep` are not accurate for most OS. The multiple call just accumulated the fixed error. See following example:

```
In [81]: %%timeit
    ...: time.sleep(0.0001)
    ...: time.sleep(0.0001)
    ...:
    ...:
31 ms ± 101 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

So the `70ms` error is reasonable, anyway the slowest example has shown the parallel cost (5.067905068397522) is better than sequential cost (5+4+3=12).

Another reason is latency of ZMQ, see [Overhead example](#Overhead)

Debug:

```shell
$ ipython -i fake_zmq_servers.py -- FakeSegmentation1 0.03
%debug
```

Related scripts: `fake_zmq_servers.py`, `fake_zmq_client.py`, `fake_launch_servers.py`, `zmq_utils.py`

## Overhead

Server just recv and send back the array, the pickle cost and transfer overhead introduced.


```shell
python zmq_overhead_test_server.py
```

```shell
python zmq_overhead_test_client.py # 2000 x 1000 x 3 uint8 array
# time_elapsed=2.25831937789917 mean=0.0225831937789917
# 22ms is... very significant anyway.
```

```shell
python zmq_overhead_test_client.py --width 800 --height 600 # 800 x 600 x 3 uint8 array
# time_elapsed=2.25831937789917 mean=0.0225831937789917
# time_elapsed=0.6016485691070557 mean=0.006016485691070557
# 6ms, it depends.
```

## Vanilla Socket Overhead

Start three servers:

```shell
python socket_overhead_multi.py server
```

Start three clients:

```shell
python socket_overhead_multi.py client
```

The output:
```
Connecting to 127.0.0.1:10002
Connecting to 127.0.0.1:10000
Connecting to 127.0.0.1:10001
Second per send_and_recv: 0.0103552674
10.355267399999999
Second per send_and_recv: 0.0156795476
15.6795476
Second per send_and_recv: 0.0164399412
16.4399412
```

Interestingly, the more process(3 *thread* is used by supervisor process to inspect 3 *processes* running the real task.) will not increase speed. So it's limited by TCP bandwidth or copy speed?

```shell
python socket_overhead_multi.py server --n-thread 1 --number 1000

python socket_overhead_multi.py client --n-thread 1 --number 1000
```

The output:
```
Connecting to 127.0.0.1:10000
Second per send_and_recv: 0.0052526566
5.2526566
```

A image is approximately `6Mb`, so a second processing `1200Mb` at most?

For some reason, `socket_overhead_multi.py` will not work in Linux.

## Baseline: multiprocessing

Use shared numpy array and multiprocessing:

```shell
$ python baseline_pool.py
```

The output:
```
mean: 0.06414416122436524 std: 0.037146757524145264 len: 250
[0.6500084400177002, 0.06398630142211914, 0.06078481674194336, 0.06593537330627441, 0.06520724296569824] ... [0.06170082092285156, 0.061620473861694336, 0.06216311454772949, 0.062009572982788086, 0.06300711631774902]
```

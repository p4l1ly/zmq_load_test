# zmq_load_test
Simple tests of ZeroMQ REQ/REP server response time, when multiple requests come from
multiple sockets created by multiple processes running on multiple machines.

There are 3 files:

**zmq_load_test.py**
Program opens multiple sockets and sends multiple random length messages with each of them.
Program accepts 3 arguments: number of sockets, number off messages per socket, maximum message length

**zmq_load_test_client.py**
Run this program on every testing machine. Program waits (as 0MQ subscriber) for starting message
containing CLI arguments for **zmq_load_test.py** plus number of process instances to run. Program measures
time of the process and pushes the data back to server.

**zmq_load_test_starter.py**
Run this program on one machine when all clients are running. Program sends starting signal
(as 0MQ publisher) to the clients, then collects the times (as 0MQ PULL) and prints the maximum of them.


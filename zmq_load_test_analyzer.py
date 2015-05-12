import subprocess, time, zmq, json, sys
from threading import Thread, Barrier

def mogrify(topic, msg):
    """ json encode the message and prepend the topic """
    return topic + ' ' + json.dumps(msg)

ctx = zmq.Context()

sender = ctx.socket(zmq.PUB)
sender.bind('tcp://*:5557')

receiver = ctx.socket(zmq.PULL)
receiver.bind('tcp://*:5558')

barrier = Barrier(2)

def senderThread():
  time.sleep(2)
  for ps in range(0, 20, 2):
    for socks in range(0, 20, 2):
      sender.send_string(mogrify('measurement_start'
                                , { 'processes':  int(ps)
                                  , 'sockets':    int(socks)
                                  , 'messages':   int(sys.argv[2])
                                  , 'max_length': int(sys.argv[3])
                                  }))
      barrier.wait()

Thread(target=senderThread).start()

for ps in range(0, 20, 2):
  for socks in range(0, 20, 2):
    res = []
    for _ in range(int(sys.argv[1])):
      res.append(receiver.recv_string())
      print('result received', file=sys.stderr)

    print(max(map(float, res)))

    barrier.wait()

import subprocess, time, zmq, json, sys
from threading import Thread

def mogrify(topic, msg):
    """ json encode the message and prepend the topic """
    return topic + ' ' + json.dumps(msg)

ctx = zmq.Context()

sender = ctx.socket(zmq.PUB)
sender.bind('tcp://*:5557')

receiver = ctx.socket(zmq.PULL)
receiver.bind('tcp://*:5558')

def senderThread():
  time.sleep(2)
  sender.send_string(mogrify('measurement_start'
                            , { 'processes':  int(sys.argv[2])
                              , 'sockets':    int(sys.argv[3])
                              , 'messages':   int(sys.argv[4])
                              , 'max_length': int(sys.argv[5])
                              }))

Thread(target=senderThread).start()

res = []
for _ in range(int(sys.argv[1])):
  res.append(receiver.recv_string())

print(max(map(float, res)))

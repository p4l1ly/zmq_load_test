import subprocess, time, zmq, json
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
  sender.send_string(mogrify('measurement_start', { 'processes':  10
                                                  , 'sockets':    10
                                                  , 'messages':   10
                                                  , 'max_length': 10
                                                  }))

Thread(target=senderThread).start()

res = []
for _ in range(4):
  res.append(receiver.recv_string())

print(max(map(float, res)))

import subprocess, time, zmq, json

def demogrify(topicmsg):
    """ Inverse of mogrify() """
    json0 = topicmsg.find('{')
    topic = topicmsg[0:json0].strip()
    msg = json.loads(topicmsg[json0:])
    return topic, msg

def measurement(params):
  tic = time.clock()

  ps = []
  for i in range(int(params['processes'])):
    ps.append(
      subprocess.Popen([ 'python3', 'zmq_load_test.py'
                       , str(int(params['sockets']))
                       , str(int(params['messages']))
                       , str(int(params['max_length']))
                       ])
    )

  for p in ps:
    p.wait()

  return time.clock() - tic

if __name__ == '__main__':
  ctx = zmq.Context()

  receiver = ctx.socket(zmq.SUB)
  receiver.connect('tcp://192.168.14.204:5557')
  receiver.setsockopt_string(zmq.SUBSCRIBE, 'measurement_start')

  print('receiver connected')

  sender = ctx.socket(zmq.PUSH)
  sender.connect('tcp://192.168.14.204:5558')

  print('sender connected')

  while True:
    topicmsg = receiver.recv_string()
    print('data received')

    _, params = demogrify(topicmsg)

    comm_time = measurement(params)
    sender.send_string(str(comm_time))
    print('result sent')

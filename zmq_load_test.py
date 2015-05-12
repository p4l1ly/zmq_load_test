import zmq, sys, random, string, os

if __name__ == '__main__':
  context = zmq.Context()
  for i in range(int(sys.argv[1])):
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://{}'.format(os.environ['ECHO_IP_PORT']))
    for i in range(int(sys.argv[2])):
      random_string = ''.join(
        random.choice(string.ascii_letters + string.digits)
          for _ in range(random.randint(0, int(sys.argv[3]))))

      socket.send_string(random_string)
      assert random_string == socket.recv_string()

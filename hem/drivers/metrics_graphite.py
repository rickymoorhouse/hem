import socket
import time

class instance(object):
    config = None
    server = None
    port = 2003

    def __init__(self, config):
        self.config = config
        self.server = config.get('server', 'localhost')
        self.port = config.get('port', 2003)


    def store(self, name, value):
        message = 'hem.{} {} {}\n'.format(name, value, int(time.time()))
        sock = socket.socket()
        sock.connect((self.server, self.port))
        sock.sendall(message)
        sock.close()

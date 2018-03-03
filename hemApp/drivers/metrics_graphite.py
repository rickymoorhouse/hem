import socket
import time
import logging
import hemApp
class instance(hemApp.Metrics):
    config = None
    server = None
    port = 2003
    cache = []

    def __init__(self, config):
        self.config = config
        self.server = config.get('server', 'localhost')
        self.port = config.get('port', 2003)
        self.logger = logging.getLogger(__name__)

    def stage(self, name, value):
        message = 'hem.{} {} {}'.format(name, value, int(time.time()))
        self.cache.append(message)
        self.logger.debug("storing {}".format(message))

    def store(self):
        sock = socket.socket()
        sock.connect((self.server, self.port))
        self.logger.info("Storing {} records".format(len(self.cache)))
        self.logger.debug("\n".join(self.cache))
        sock.sendall("\n".join(self.cache))        
        sock.close()
        # Clear out cache
        self.cache[:] = []

    def __del__(self):
        logging.info("Storing remaining data ({} records)".format(len(self.cache)))
        self.store()
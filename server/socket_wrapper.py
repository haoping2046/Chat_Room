

class SocketWrapper(object):

    def __init__(self, sock):
        self.sock = sock

    def recv_data(self):
        """receive data and decode to string"""
        try:
            return self.sock.recv(512).decode('utf-8')
        except:
            return ''

    def send_data(self, message):
        """send data and encode"""
        return self.sock.send(message.encode('utf-8'))

    def close(self):
        self.sock.close()
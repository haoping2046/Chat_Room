import socket
from config_basic import *

class ClientSocket(socket.socket):

    def __init__(self):
        # set TCP
        super(ClientSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)

    def connect_server(self):
        super(ClientSocket, self).connect((SERVER_IP, SERVER_PORT))

    def recv_data(self):
        """receive data and decode to string"""
        try:
            return self.recv(512).decode('utf-8')
        except:
            return ''

    def send_data(self, message):
        """send data and encode"""
        self.send(message.encode('utf-8'))
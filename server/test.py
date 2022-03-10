import socket
from socket_wrapper import SocketWrapper

def test():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8050))

    while True:
        msg = input('Please input message: ')
        if not msg:
            print('Message cannot be empty')
            continue

        client_socket.send(msg.encode('utf-8'))
        print(client_socket.recv(512).decode(('utf-8')))

    client_socket.close()

if __name__ == '__main__':
    test()


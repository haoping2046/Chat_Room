from server_socket import ServerSocket
from socket_wrapper import SocketWrapper
from threading import Thread
from config_basic import *
from response_protocol import *
from db import DB

class Server(object):

    def __init__(self):
        self.server_socket = ServerSocket()

        # use dict to associate id and function
        self.request_handle_func = {}
        self.register(REQUEST_LOGIN, self.request_login_handle)
        self.register(REQUEST_CHAT, self.request_chat_handle)

        # store user to dictionary
        self.client = {}

        # db
        self.db = DB()

    def register(self, request_id, handle_func):
        self.request_handle_func[request_id] = handle_func

    def startup(self):
        while True:
            print("Waiting for client connection ")
            soc, addr = self.server_socket.accept()
            print("Receive a client connection ")

            client_soc = SocketWrapper(soc)

            # create thread to handle multiple client
            # t = Thread(target=self.request_handle, args=(client_soc,)) # add , if it just has one data
            # t.start()
            Thread(target=lambda: self.request_handle(client_soc)).start()

    def request_handle(self, client_soc):
        # receive multiple msg from one client
        while True:
            recv_data = client_soc.recv_data()
            if not recv_data:
                self.remove_offline_user(client_soc)
                client_soc.close()
                break

            # Parse data
            parse_data = self.parse_request_data(recv_data)

            # Call func depends on type
            handle_function = self.request_handle_func.get(parse_data['request_id'])
            if handle_function:
                handle_function(client_soc, parse_data)
            else:
                print('id is wrong')

    def remove_offline_user(self, client_soc):
        print('A client is offline')
        for username, info in self.client.items():
            if info['sock'] == client_soc:
                print('Before remove offline user')
                print(self.client)
                del self.client[username]
                print('After remove offline user')
                print(self.client)
                break

    def parse_request_data(self, recv_data):
        """
        data format:
        request of login format: 0001|username|password
        request of chat message format: 0002|username|messages
        """
        req_list = recv_data.split(DELIMITER)
        req_data = {'request_id': req_list[0]}

        if req_data['request_id'] == REQUEST_LOGIN:
            req_data['username'] = req_list[1]
            req_data['password'] = req_list[2]
        elif req_data['request_id'] == REQUEST_CHAT:
            req_data['username'] = req_list[1]
            req_data['message'] = req_list[2]

        return req_data

    def request_login_handle(self, client_soc, req_data):
        username = req_data['username']
        password = req_data['password']

        res, nickname, username = self.check_login(username, password)

        # If the user exists, add socket and nickname to the client dict
        if res == '1':
            self.client[username] = {'sock': client_soc, 'nickname': nickname}

        response_text = ResponseProtocol.response_login_result(res, nickname, username)
        print('Send: ' + response_text)
        client_soc.send_data(response_text)

    def request_chat_handle(self, client_soc, req_data):
        # login in u1, then use test case: 0002|u1|hello
        # output: 1002|n1|hello

        username = req_data['username']
        msg = req_data['message']
        nickname = self.client[username]['nickname']

        response_msg = ResponseProtocol.response_chat(nickname, msg)
        print('Send: ' + response_msg)
        # send msg to online users except itself
        for u_name, info in self.client.items():
            if u_name == username:
                continue
            info['sock'].send_data(response_msg)

    def check_login(self, username, password):
        # test case: 0001|u1|111,  0001|u1|222
        # output: 1001|1|n1|u1, 1001|0||u1

        res = self.db.get_one("select * from user where user_name = '%s'" % username)

        if not res: return '0', '', username

        if password != res['user_password']: return '0', '', username

        return '1', res['user_nickname'], res['user_name']


if __name__ == '__main__':
    Server().startup()
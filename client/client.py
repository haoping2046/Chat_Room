from window_login import WindowLogin
from request_protocol import RequestProtocol
from client_socket import ClientSocket
from threading import Thread
from config_basic import *
from tkinter.messagebox import showinfo
from window_chat import WindowChat
import sys

class Client(object):

    def __init__(self):
        self.window = WindowLogin()
        self.window.on_click_reset(self.window.clear)
        self.window.on_click_login(self.send_login_data)
        self.window.on_window_closed(self.exit)

        self.window_chat = WindowChat()
        self.window_chat.withdraw()  # hidden
        self.window_chat.on_click_send_btn(self.send_chat_data)
        self.window_chat.on_window_closed(self.exit)

        self.client_socket = ClientSocket()

        self.response_handle_func = {}
        self.register(RESPONSE_LOGIN_RESULT, self.response_login_handle)
        self.register(RESPONSE_CHAT, self.response_chat_handle)

        self.username = None  # Save username in order to send message

        self.is_running = True  # flag that program is running

    def register(self, request_id, handle_func):
        self.response_handle_func[request_id] = handle_func

    def startup(self):
        self.client_socket.connect_server()
        # create thread to receive multiple messages
        Thread(target=self.response_handle).start()
        self.window.mainloop()


    def send_login_data(self):
        username = self.window.get_username()
        password = self.window.get_password()

        # generate protocol string
        request_text = RequestProtocol.request_login_result(username, password)

        print('Send: ' + request_text)
        self.client_socket.send_data(request_text)

    def send_chat_data(self):
        msg = self.window_chat.get_input()
        self.window_chat.clear()

        request_text = RequestProtocol.request_chat(self.username, msg)

        self.client_socket.send_data(request_text)

        # display my message in my chat text area
        self.window_chat.append_msg('Me', msg)

    def response_handle(self):
        # Handle message from server
        while self.is_running:
            recv_data = self.client_socket.recv_data()
            print('Receive: ' + recv_data)

            # parse message
            response_data = self.parse_response_data(recv_data)

            # handle login or chat func
            handle_func = self.response_handle_func[response_data['response_id']]
            if handle_func:
                handle_func(response_data)

    def parse_response_data(self, recv_data):
        # login response: 1001|1|n1|u1, 1001|0||u1
        # chat response: 1002|n1|hello
        recv_data_list = recv_data.split(DELIMITER)
        response_data = dict()
        response_data['response_id'] = recv_data_list[0]

        if response_data['response_id'] == RESPONSE_LOGIN_RESULT:
            response_data['result'] = recv_data_list[1]
            response_data['nickname'] = recv_data_list[2]
            response_data['username'] = recv_data_list[3]
        elif response_data['response_id'] == RESPONSE_CHAT:
            response_data['nickname'] = recv_data_list[1]
            response_data['message'] = recv_data_list[2]

        return response_data

    def response_login_handle(self, response_data):
        res = response_data['result']
        if res == '0':
            showinfo('Login', 'Fail, username or password is not correct!')
            return

        showinfo('Login', 'Success!')

        self.username = response_data['username']
        nickname = response_data['nickname']
        self.window_chat.set_title(nickname)
        self.window_chat.update()
        self.window_chat.deiconify()  # display window
        self.window.withdraw()

    def response_chat_handle(self, response_data):
        msg = response_data['message']
        sender = response_data['nickname']
        self.window_chat.append_msg(sender, msg)

    def exit(self):
        #  click x to exit program
        self.is_running = False  # stop sub-thread
        self.client_socket.close()
        sys.exit(0)

if __name__ == '__main__':
    client = Client()
    client.startup()
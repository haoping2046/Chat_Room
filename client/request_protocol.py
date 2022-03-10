from config_basic import *


class RequestProtocol(object):

    # request of login format: 0001|username|password
    # request of chat message format: 0002|username|messages

    @staticmethod
    def request_login_result(username, password):
        return DELIMITER.join([REQUEST_LOGIN, username, password])

    @staticmethod
    def request_chat(username, messages):
        return DELIMITER.join([REQUEST_CHAT, username, messages])
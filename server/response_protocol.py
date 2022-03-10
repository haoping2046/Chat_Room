from config_basic import *


class ResponseProtocol(object):

    # response of login format: 1001|res|nickname|username
    # response of chat message format: 1002|nickname|messages

    @staticmethod
    def response_login_result(res, nickname, username):
        """
        Generate a string of login result
        :param res: 0 is fail, 1 is success
        :param nickname:
        :param username:
        :return: a string of response of login
        """
        return DELIMITER.join([RESPONSE_LOGIN_RESULT, res, nickname, username])

    @staticmethod
    def response_chat(nickname, messages):
        """
        Send a message string to user
        :param nickname:
        :param messages:
        :return: a string of user's message
        """
        return DELIMITER.join([RESPONSE_CHAT, nickname, messages])
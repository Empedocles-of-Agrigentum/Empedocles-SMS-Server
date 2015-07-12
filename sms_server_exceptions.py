# -*- coding:utf-8 -*-

import exceptions


class SMSServerException(exceptions.Exception):
    def __init__(self):
        pass

    def __str__(self):
        return "Some undefined error while executing SMS server!"


class SMSServerConfigException(SMSServerException):
    def __init__(self, message):
        self._message_ = message

    def __str__(self):
        return self._message_


class SMSServerModemException(SMSServerException):
    def __init__(self, message):
        self._message_ = message

    def __str__(self):
        return self._message_

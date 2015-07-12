# -*- coding:utf-8 -*-

import threading


class SharedData:
    def __init__(self, config):
        self._sms_queue_ = []
        self._config_ = config
        self._status_ = {"delivery": "off",
                         "network": "off"}
        self._mutex_ = threading.RLock()

    def push_message(self, mes):
        self._mutex_.acquire()
        self._sms_queue_.append(mes)
        self._mutex_.release()

    def pop_message(self):
        self._mutex_.acquire()
        try:
            result = self._sms_queue_.pop(0)
        except IndexError, e:
            result = None
        self._mutex_.release()
        return result

    def get_config(self):
        self._mutex_.acquire()
        result = self._config_
        self._mutex_.release()
        return result

    def get_status(self, module="none"):
        if module == "delivery":
            if self._status_["delivery"] == "on":
                return True
            else:
                return False
        elif module == "network":
            if self._status_["network"] == "on":
                return True
            else:
                return False
        else:
            return False

    def enable(self, module="none"):
        if module == "delivery":
            self._status_["delivery"] = "on"
        elif module == "network":
            self._status_["network"] = "on"

    def disable(self, module="none"):
        if module == "delivery":
            self._status_["delivery"] = "off"
        elif module == "network":
            self._status_["network"] = "off"

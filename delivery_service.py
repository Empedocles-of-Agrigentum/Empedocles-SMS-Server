# -*- coding:utf-8 -*-

import threading
import sys
import time

import modem_driver


class DeliveryService(threading.Thread):
    def __init__(self, shared_data):
        sys.stdout.write("Initializing delivery service..." + "\n")
        threading.Thread.__init__(self)
        self._shared_data_ = shared_data
        self._config_ = shared_data.get_config()
        self._modems_ = []
        sys.stdout.write("Initializing modems..." + "\n")
        self._wake_the_modems_()

    def _select_modem_(self, dest):
        return 0

    def _is_running_(self):
        return self._shared_data_.get_status("delivery")

    def run(self):
        sys.stdout.write("Delivery is waiting for messages\n")
        while self._is_running_():
            while True:
                mes = self._shared_data_.pop_message()
                if mes is not None:
                    dest = mes["destination"]
                    text = mes["text"]
                    sys.stdout.write("Got message for " + dest + "\n")
                    modem_num = self._select_modem_(dest)
                    self._modems_[modem_num].send_sms(dest, text)
                else:
                    break
            time.sleep(1)

    def _wake_the_modems_(self):
        for i in range(self._config_.get_modems_count()):
            try:
                sys.stdout.write("Modem at " + self._config_.get_modem_info(i)["port"] + "\n")
                cur_modem = modem_driver.DriverDetector.detect(self._config_.get_modem_info(i))
                self._modems_.append(cur_modem)
                sys.stdout.write("Success at " + self._config_.get_modem_info(i)["port"] + "\n")
            except:
                sys.stdout.write("Fail at " + self._config_.get_modem_info(i)["port"] + "\n")
                self._modems_.append(modem_driver.DummyModem())

# -*- coding:utf-8 -*-

import sys

import shared_data
import network_service
import delivery_service


class SMSServer:
    def __init__(self, srv_config):
        sys.stdout.write("Reading config... ")
        self._config_ = srv_config
        self._shared_data_ = shared_data.SharedData(self._config_)
        sys.stdout.write("OK\n")
        sys.stdout.write("Initializing modules...\n")
        self._network_service_ = network_service.NetworkService(self._shared_data_)
        self._delivery_service = delivery_service.DeliveryService(self._shared_data_)
        sys.stdout.write("OK\n")

    def start(self):
        sys.stdout.write("Enabling modules...\n")
        self._shared_data_.enable(module="network")
        self._shared_data_.enable(module="delivery")
        sys.stdout.write("OK\n")
        sys.stdout.write("Starting modules...\n")
        self._network_service_.start()
        self._delivery_service.start()
        sys.stdout.write("OK\n")

    def stop(self):
        sys.stdout.write("Disabling modules... ")
        self._shared_data_.disable(module="network")
        self._shared_data_.disable(module="delivery")
        sys.stdout.write("OK\n")
        sys.stdout.write("Waiting for threads to stop... ")
        self._network_service_.join()
        self._delivery_service.join()
        sys.stdout.write("OK\n")
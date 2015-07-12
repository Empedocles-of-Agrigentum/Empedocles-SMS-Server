# -*- coding:utf-8 -*-

import copy
import json

import sms_server_exceptions


class ConfigReader:
    def __init__(self, path):
        self.conf_file = None
        self.conf_dict = None
        try:
            self.conf_file = open(path)
        except:
            raise sms_server_exceptions.SMSServerConfigException("Error opening config file!")
        self.conf_dict = json.loads(self.conf_file.read(), encoding="utf-8")

    def get_conf_dict(self):
        return self.conf_dict


class Config:
    def __init__(self, config_dict):
        self._config_dict_ = copy.deepcopy(config_dict)
        if self._basic_check_():
            if self._advanced_check_():
                pass
            else:
                raise sms_server_exceptions.SMSServerConfigException(
                    "Invalid JSON-object: missing parameter!")
        else:
            raise sms_server_exceptions.SMSServerConfigException("Invalid JSON-object: missing root key!")

    def _basic_check_(self):
        basic_keys = ["network", "security", "users", "modems"]
        for k in basic_keys:
            if k not in self._config_dict_:
                return False
        return True

    # TODO: дописать проверку корректности данных для каждого пользователя и модема
    def _advanced_check_(self):
        network_keys = ["port"]
        security_keys = ["auth_state", "cipher_state"]
        for k in network_keys:
            if k not in self._config_dict_["network"]:
                return False
        for k in security_keys:
            if k not in self._config_dict_["security"]:
                return False
        return True

    def get_network_port(self):
        return int(self._config_dict_["network"]["port"])

    def get_security_auth_state(self):
        return self._config_dict_["security"]["auth_state"]

    def get_security_cipher_state(self):
        return self._config_dict_["security"]["cipher_state"]

    def get_users_count(self):
        return len(self._config_dict_["users"])

    def get_user_login(self, usr_num):
        return self._config_dict_["users"][str(usr_num)]["login"]

    def get_user_password(self, usr_num):
        return self._config_dict_["users"][str(usr_num)]["login"]

    def get_modems_count(self):
        return len(self._config_dict_["modems"])

    def get_modem_info(self, modem_num):
        if (modem_num >= 0) & (modem_num < self.get_modems_count()):
            return self._config_dict_["modems"][str(modem_num)]
        else:
            return None

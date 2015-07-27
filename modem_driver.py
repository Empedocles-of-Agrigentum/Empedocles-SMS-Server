# -*- coding:utf-8 -*-

import sys

import serial
import smspdu

import sms_server_exceptions


class DriverDetector:
    def __init__(self):
        pass

    @staticmethod
    def detect(modem_info):
        if modem_info["driver"] == "huawei_e173":
            return HuaweiE173(modem_info["port"], modem_info["pin"])
        else:
            return None


class ModemDriver:
    def __init__(self):
        self._dongle = None
        self._pin = None

    def send_sms(self, phone_number, sms_text, mode="text"):
        """Send SMS"""
        pass

    def initialize_dongle(self, pin_code="0000"):
        """Initialize dongle"""
        pass

    def _encode_to_pdu_(self, phone_number, sms_text):
        """Convert message to PDU"""
        pass


class DummyModem(ModemDriver):
    def __init__(self):
        ModemDriver.__init__(self)

    def send_sms(self, phone_number, sms_text, mode="text"):
        pass

    def initialize_dongle(self, pin_code="0000"):
        pass

    def _encode_to_pdu_(self, phone_number, sms_text):
        pass


class HuaweiE173(ModemDriver):
    def __init__(self, port_id, pin_code):
        ModemDriver.__init__(self)
        try:
            self._dongle = serial.Serial(port_id, baudrate=9600, timeout=5)
            self._pin = pin_code
            self.initialize_dongle(self._pin)
        except:
            raise sms_server_exceptions.SMSServerModemException("No device on " + port_id)

    def send_sms(self, phone_number, sms_text, mode="text"):
        if mode == "text":
            self._send_sms_text_(phone_number, sms_text)
        elif mode == "pdu":
            self._send_sms_pdu_(phone_number, sms_text)

    def initialize_dongle(self, pin_code="0000"):
        sys.stdout.write("Initializing dongle...")
        self._dongle.write("AT+CPIN?\r")
        response = self._dongle.read(16)
        sys.stdout.write("Got response " + response)
        if response != "+CPIN: READY":
            self._dongle.write("AT+CPIN=" + "\"" + pin_code + "\"" + "\r")
            self._dongle.read(16)

    def _encode_to_pdu_(self, phone_number, sms_text):
        mes_pdu = smspdu.SMS_DELIVER.create(sender="0000000000", recipient=phone_number, user_data=sms_text)
        return mes_pdu.toPDU()

    def _send_sms_text_(self, phone_number, sms_text):
        self._dongle.write("AT+CMGF=1\r")
        self._dongle.read(16)
        self._dongle.write("AT+CMGS=" + "\"" + phone_number + "\"" + "\r")
        self._dongle.read(16)
        self._dongle.write(sms_text + chr(26))
        self._dongle.read(16)

    def _send_sms_pdu_(self, phone_number, sms_text):
        self._dongle.write("AT+CMGF=0\r")
        self._dongle.read(16)
        sms_text = self._encode_to_pdu_(phone_number, sms_text)
        self._dongle.write("AT+CMGS=" + str(len(sms_text)) + "\r")
        self._dongle.read(16)
        self._dongle.write(sms_text + chr(26))
        self._dongle.read(16)

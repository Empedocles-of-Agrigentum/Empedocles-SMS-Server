# -*- coding:utf-8 -*-

import json
import threading
import sys
import os

import twisted.web.resource
import twisted.web.server
import twisted.internet.reactor


class NetworkParser:
    def __init__(self):
        pass

    @staticmethod
    def parse_message(net_message):
        try:
            mes_dict = json.loads(net_message, encoding="utf-8")
        except ValueError, e:
            mes_dict = None
        return mes_dict


class ServerInfoResource(twisted.web.resource.Resource):
    def render_GET(self, request):
        html_head = "<head><meta charset=\"UTF-8\"><title>Server info</title></head>"
        html_body = "<body><h3>SMS Server</h3><p>is running on pid: " + str(os.getpid()) + "</p></body>"
        full_page = "<html>" + html_head + html_body + "</html>"
        return full_page


class ServerSendResource(twisted.web.resource.Resource):
    def __init__(self, shared_data):
        twisted.web.resource.Resource.__init__(self)
        self._shared_data_ = shared_data

    def render_POST(self, request):
        mes = request.content.read()
        sys.stdout.write("Recieved " + mes + "\n")
        self._shared_data_.push_message(NetworkParser.parse_message(mes))


class NetworkService(threading.Thread):
    def __init__(self, shared_data):
        threading.Thread.__init__(self)
        self._shared_data_ = shared_data
        self._config_ = shared_data.get_config()
        self._build_site_structure_()

    def _build_site_structure_(self):
        site_root = twisted.web.resource.Resource()
        site_root.putChild("info", ServerInfoResource())
        site_root.putChild("send_sms", ServerSendResource(self._shared_data_))
        factory = twisted.web.server.Site(site_root)
        twisted.internet.reactor.listenTCP(self._config_.get_network_port(), factory)

    def _is_running_(self):
        return self._shared_data_.get_status("network")

    def run(self):
        twisted.internet.reactor.run()
        while self._is_running_():
            pass
        twisted.internet.reactor.stop()

"""
https://www.myfreecams.com/_js/serverconfig.js
- websocket_servers

https://www.myfreecams.com/js/wsgw.js
- function wsgw_connect
- function zgw_TxLogin

https://www.myfreecams.com/js/FCS.js
FCTYPE_LOGIN = 1
FCTYPE_USERNAMELOOKUP = 10
FCTYPE_LOGOUT = 99
FCVIDEO_TX_IDLE = 0
"""

import random
import re

from streamlink.plugin import Plugin
from streamlink.stream import HLSStream

try:
    from websocket import create_connection
    HAS_WEBSOCKET = True
except ImportError:
    HAS_WEBSOCKET = False

HLS_VIDEO_URL = "http://video{0}.myfreecams.com:1935/NxServer/ngrp:mfc_{1}.f4v_mobile/playlist.m3u8"
WEBSOCKET_SERVERS = [7, 8, 9, 10, 11, 12, 20, 22, 23, 24, 25, 26, 27, 28, 29, 39]

_url_re = re.compile(r"https?\:\/\/(?:\w+\.)?myfreecams\.com\/\#(?P<username>\w+)")


class MyFreeCams(Plugin):
    @classmethod
    def can_handle_url(cls, url):
        return _url_re.match(url)

    def _get_streams(self):
        match = _url_re.match(self.url)
        username = match.group("username")

        if not HAS_WEBSOCKET:
            self.logger.error("websocket-client is not installed")
            self.logger.info("You can install it with:")
            self.logger.info("pip install websocket-client")
            self.logger.info("https://pypi.python.org/pypi/websocket-client")
            return

        _data_channel_re = re.compile(r"""
            %22nm%22:%22(?P<username>{0})%22
            .+
            %22uid%22\:(?P<uid>[\d]+)\,
            %22vs%22\:(?P<vs>[\d]+)\,
            .+
            %22camserv%22\:(?P<server>[\d]+)
            """.format(username), re.VERBOSE)

        xchat = "xchat{0}".format(random.choice(WEBSOCKET_SERVERS))
        ws_host = "wss://{0}.myfreecams.com/fcsl".format(xchat)
        ws = create_connection(ws_host)

        send_msg_hello = "hello fcserver\n\0"
        send_msg_login = "1 0 0 20071025 0 guest:guest\n\0"
        send_msg_data = "10 0 0 20 0 {0}\n\0".format(username)
        send_msg_logout = "99 0 0 0 0"

        ws.send(send_msg_hello)
        ws.send(send_msg_login)
        ws.send(send_msg_data)

        data_ws = ws.recv()
        loop_number = 0
        status_regex = False
        while status_regex is not True:
            if loop_number is 15:
                self.logger.error("Stream is offline or username is invalid - {0}".format(username))
                return

            try:
                data_channel = _data_channel_re.search(data_ws)

                uid = int(data_channel.group("uid")) + 100000000
                vs = int(data_channel.group("vs"))
                camserver = int(data_channel.group("server"))

                if camserver:
                    status_regex = True
            except:
                ws.send(send_msg_data)
                data_ws = ws.recv()
                loop_number += 1
                self.logger.debug("-- RESEND WEBSOCKET DATA -- {0} --".format(loop_number))

        ws.send(send_msg_logout)
        ws.close()

        self.logger.debug("UID: {0}".format(uid))
        self.logger.debug("VS - FCVIDEO: {0}".format(vs))
        self.logger.debug("CAMSERVER: {0}".format(camserver))

        if vs is 0:
            if camserver >= 840:
                server = camserver - 500
            elif camserver < 839:
                server = 0

            self.logger.debug("VIDEO SERVER: {0}".format(server))

            if server:
                hls_url = HLS_VIDEO_URL.format(server, uid)

                self.logger.debug(hls_url)

                for s in HLSStream.parse_variant_playlist(self.session, hls_url).items():
                    yield s

__plugin__ = MyFreeCams

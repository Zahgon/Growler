
import io
import sys
import json
import time
import growler

from pathlib import Path
from itertools import chain
from datetime import datetime
from collections import OrderedDict
from growler.http import HttpStatus
from growler.utils.event_manager import Events
from wsgiref.handlers import format_date_time as format_RFC_1123


class HTTPResponse:
    SERVER_INFO = 'Growler/{growler_version} Python/{py_version}'.format(
        py_version=".".join(map(str, sys.version_info[:2])),
        growler_version=growler.__version__,
    )

    protocol = None
    has_sent_continue = False
    has_sent_headers = False
    has_ended = False
    status_code = 200
    headers = None
    message = ''
    EOL = ''
    phrase = None

    def __init__(self, protocol, EOL="\r\n"):
        self.protocol = protocol
        self.EOL = EOL

        self.headers = Headers()
        self.events = Events()

    def _set_default_headers(self):
        pass

    def send_headers(self):
        pass

    def write(self, msg=None):
        pass

    def write_eof(self):
        pass

    @property
    def status_line(self):
        pass

    def end(self):
        pass

    def redirect(self, url, status=None):
        pass

    def set(self, header, value=None):
        pass

    def header(self, header, value=None):
        pass

    def set_type(self, res_type):
        pass

    def get(self, field):
        pass


    def location(self, location):
        pass

    def links(self, links):
        pass

    def json(self, body, status=200):
        pass

    def send_json(self, obj, status=200):
        pass

    def send_html(self, html, status=200):
        pass

    def send_text(self, txt, status=200):
        pass

    def send_file(self, filename, status=200):
        pass

    def send_continue_message(self):
        pass

    def send(self, *args, **kwargs):
        raise NotImplementedError

    @property
    def info(self):
        pass

    @property
    def stream(self):
        pass

    @property
    def app(self):
        pass

    @staticmethod
    def get_current_time():
        pass


class Headers:

    EOL = '\r\n'

    def __init__(self, headers={}, **kw_headers):
        """
        Construct a headers object.

        The constructor provides the same interface as the standard
        dict constructor.

        The default value is an empty container, which will .

        """
        self._header_data = OrderedDict()
        headers = dict(headers)
        headers.update(kw_headers)
        for key, value in headers.items():
            self[key] = value

    def __getitem__(self, key):
        ci_key = self.escape(key).casefold()
        return self._header_data[ci_key][1]

    def __setitem__(self, key, value):
        key = self.escape(key)
        ci_key = key.casefold()
        self._header_data[ci_key] = (key, value)

    def __delitem__(self, key):
        key = self.escape(key)
        ci_key = key.casefold()
        del self._header_data[ci_key]

    def setdefault(self, key, default=None):
        pass

    def update(self, *args, **kwargs):
        pass

    def add_header(self, key, value, **params):
        pass

    def stringify(self, use_bytes=False):
        pass

    @staticmethod
    def escape(value):
        return value.replace("\n", r"\n")

    @staticmethod
    def de_quote(value):
        pass

    def __str__(self):
        return self.stringify()


import re
from urllib.parse import (unquote, urlparse, parse_qs)

from .methods import HTTPMethod

from growler.http.errors import (
    HTTPErrorNotImplemented,
    HTTPErrorBadRequest,
    HTTPErrorInvalidHeader,
    HTTPErrorVersionNotSupported,
)

INVALID_CHAR_REGEX = re.compile(r'[\x00-\x1F\x7F\(\),/:;<=>?@\[\]\{\} \t\\\\\"]')

MAX_REQUEST_LENGTH = 1024 ** 2  # 1 MB
MAX_REQUEST_LINE_LENGTH = 8 * 1024  # 8 KB


class Parser:
    EOL_TOKEN = None
    HTTP_VERSION = None

    def __init__(self, parent):
        """
        Construct HTTP parser.

        Parameters:
            parent (growler.HTTPResponder): The 'parent' responder which
                will forward client data to the parser, and the parser will
                send parsed data back to this object.
        """
        self.parent = parent
        self._buffer = bytearray()

        self.encoding = 'utf-8'
        self.headers = dict()

        self._http_parser = self._http_parser()
        self._http_parser.send(None)

    def consume(self, data):
        pass

    def _http_parser(self):
        pass

    def _receive_eol_token(self):
        pass

    def _parse_and_store_req_line(self, eol):
        pass

    def _parse_and_store_headers(self):
        pass

    def _store_header(self):
        pass

    def _next_header_line(self):
        pass

    def _store_request_line(self, req_line):
        pass

    @staticmethod
    def determine_newline(data):
        pass

    def split_header_key_value(self, line):
        pass

    @staticmethod
    def is_invalid_header_name(header):
        pass

    def process_get_headers(self, data):
        """
        Called upon receiving a GET HTTP request to do specific 'GET'
        things to the list of headers.
        Currently does nothing.
        """
        pass

    def process_post_headers(self, data):
        """
        Called upon receiving a POST HTTP request to do specific 'POST'
        things to the headers.
        Currently does nothing.
        """
        pass

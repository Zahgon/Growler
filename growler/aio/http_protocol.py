
import traceback
from sys import stderr
try:
    from asyncio import create_task, Future
except ImportError:
    from asyncio import ensure_future as create_task, Future  # type: ignore

from .protocol import GrowlerProtocol
from growler.http.responder import GrowlerHTTPResponder
from growler.http.response import HTTPResponse
from growler.http.errors import (
    HTTPError
)


class GrowlerHTTPProtocol(GrowlerProtocol):

    def __init__(self, app, loop=None):
        """
        Construct a GrowlerHTTPProtocol object.

        This should only be called from a growler.HTTPServer
        instance (or any asyncio.create_server function).

        Parameters
        ----------
        app : growler.Application
            Typically a growler application which is the 'target object' of
            this protocol. Any callable with a 'loop' attribute and a
            handle_client_request coroutine method should work.
        """
        self.http_application = app
        self.client_method = None
        self.client_query = None
        self.client_headers = None

        super().__init__(_loop=loop,
                         responder_factory=self.http_responder_factory)

    @staticmethod
    def http_responder_factory(proto):
        pass

    def handle_error(self, error):
        pass

    def begin_application(self, req, res):
        pass

    def body_storage_pair(self):
        pass

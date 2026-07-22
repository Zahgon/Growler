
from .parser import Parser
from .request import HTTPRequest
from .response import HTTPResponse
from .methods import HTTPMethod
from ..responder import GrowlerResponder
from .errors import (
    HTTPErrorBadRequest,
)


class GrowlerHTTPResponder(GrowlerResponder):

    body_buffer = None
    content_length = None

    def __init__(self,
                 handler,
                 parser_factory=Parser,
                 request_factory=HTTPRequest,
                 response_factory=HTTPResponse,
                 ):
        """
        Construct a Responder. This method only requires the 'parent'
        handler object which has a link to the main
        :class:`Application` object.

        Parameters:
            handler (growler.ResponderHandler): The owner/creator of
                this responder.
                This object is required to have an `app` attribute that
                points to the growler application.
                Some connection information properties (e.g. client's
                ip address) from the handler is exposed by this
                responder.

            parser_factor (type or callable): Factory function (or
                classname) of the object responsible for parsing the
                client's request line and headers. Default value is
                the :class:`growler.http.parser.Parser` class.
                The object must have a :method:`consume` method which
                accepts the incoming data.
                If this data only has partial headers, ``consume``
                returns None, and the parser should expect consume to
                be called again.
                When the headers have finished, the consume function
                returns any body data past the headers.

            request_factory (type or callable): Factory function (or
                classname) of the request object which gets passed to
                the applications middleware as the first parameter.
                The default value is the class
                :class:`growler.http.HTTPRequest`.
                When called, this object must accepts two arguments:
                this responder's handler and the headers returned
                from the parser object.

            response_factory (type or callable): Factory function (or
                classname) of the response object which gets passed to
                the application's middleware as the second parameter.
                The default value is the class :class:`HTTPResponse`
                found in :mod:`growler.http`.
                The function is called with this responder's handler
                object, which provides access to the 'write stream'
                to respond.

        """
        self._handler = handler
        self.parser = parser_factory(self)
        self.build_req = request_factory
        self.build_res = response_factory

    def on_data(self, data):
        pass

    def begin_application(self, req, res):
        pass

    def set_body_data(self, data):
        pass

    def set_request_line(self, method, url, version):
        pass

    def init_body_buffer(self, method, headers):
        pass

    def build_req_and_res(self):
        pass

    def validate_and_store_body_data(self, data):
        pass

    def body_storage_pair(self):
        pass

    @property
    def method(self):
        pass

    @property
    def method_str(self):
        pass

    @property
    def parsed_query(self):
        pass

    @property
    def headers(self):
        pass

    @property
    def loop(self):
        pass

    @property
    def app(self):
        pass

    @property
    def ip(self):
        pass

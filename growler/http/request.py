
import logging

logger = logging.getLogger(__name__)


class HTTPRequest:

    _responder = None
    headers = None
    _body = None

    def __init__(self, responder, headers):
        """
        The HTTPRequest object is all the information you could want
        about the incoming http connection.
        It gets passed along with the HTTPResponse object to all the
        middleware of the app.

        Parameters:
            responder (GrowlerHTTPResponder): A reference to the
                responder object responsible for handling the
                client's request and creating this HTTPRequest object.
            headers (dict): The headers gathered from the incoming
                stream.
        """
        self.log = logger.getChild("id=%x" % id(self))
        self._responder = responder
        self.headers = headers

        if 'CONTENT-LENGTH' in headers:
            self._body, self._body_writer = responder.body_storage_pair()

        self.log.info("%r %r", self.method, self.path)

    def param(self, name, default=None):
        pass

    async def body(self):
        pass

    def set_body_data(self, data):
        pass

    def type_is(self, mime_type):
        pass

    @property
    def ip(self):
        pass

    @property
    def app(self):
        pass

    @property
    def path(self):
        pass

    @property
    def originalURL(self):
        pass

    @property
    def loop(self):
        pass

    @property
    def query(self):
        pass

    @property
    def hostname(self):
        pass

    @property
    def method(self):
        pass

    @property
    def protocol(self):
        pass

    @property
    def peercert(self):
        pass

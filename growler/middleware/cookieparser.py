
import json
import logging
from http.cookies import SimpleCookie

logger = logging.getLogger(__name__)


class CookieParser:

    def __init__(self, **opts):
        """
        Construct a CookieParser with optional 'opts' keyword arguments. These
        do nothing currently except get stored in the CookieParser.opts
        attribute.
        """
        self.log = logger.getChild("id=%x" % id(self))
        self.log.info("Initialized with %s", json.dumps(opts))
        self.opts = opts

    def __call__(self, req, res):
        """
        Parses cookies of the header request (using the 'cookie' header key)
        and adds a callback to the 'on_headerstrings' response event.
        """
        if hasattr(req, 'cookies'):
            return

        req.cookies, res.cookies = SimpleCookie(), SimpleCookie()

        req.cookies.load(req.headers.get('COOKIE', ''))

        def _gen_cookie():
            pass

        res.headers['Set-Cookie'] = _gen_cookie

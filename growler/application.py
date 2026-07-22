
import os
import sys
import types
import inspect
import logging

from .utils.event_manager import Events
from .routing import Router, RouterMeta, MiddlewareChain

from .http import (
    HTTPRequest,
    HTTPResponse,
    HTTPMethod,
)

logger = logging.getLogger(__name__)


class GrowlerStopIteration(StopIteration):
    pass


class Application:

    error_recursion_max_depth = 10

    def __init__(self,
                 name=__name__,
                 debug=True,
                 request_class=HTTPRequest,
                 response_class=HTTPResponse,
                 middleware_chain=None,
                 **kw):
        """
        Creates an application object.

        Args:
            name (str): Does nothing right now except identify object

            debug (bool): (de)Activates the loop's debug setting

            request_class (type or callable): The factory of request
                objects, the default of which is
                :class:`growler.HTTPRequest`.
                This should only be set in special cases, like
                debugging or if the dev doesn't want to modify
                default request objects via middleware.

            response_class (type or callable): The factory of
                response objects, the default of which is
                :class:`growler.HTTPResponse`.
                This should only be set in special cases, like
                debugging or if the dev doesn't want to modify
                default response objects via middleware.

            middleware_chain (type or callable): If a type or
                function-like object, it will be called and the
                return value will be interpreted as the middleware
                chain.
                Otherwise, if not None, it will use the argment as
                the middleware chain.
                The default value, if parameter is `None`, is the
                :class:`MiddlewareChain` class.
                This value is accessible via the attribute
                :attr:`middleware`.

        Keyword Args:
            Any other custom variables for the application.
            This dict is stored as the attribute 'config' in the
            application.
            These variables are accessible by the application's
            dict-access, as in:

                .. code:: python

                    app = App(..., val='VALUE')
                    app['val'] #=> VALUE
        """
        self.name = name

        self.config = {
            'x-powered-by': True,
            'env': os.getenv('GROWLER_ENV', 'development')
        }
        self.config.update(kw)

        if middleware_chain is None:
            middleware_chain = MiddlewareChain()
        elif isinstance(middleware_chain, (types.FunctionType, type)):
            middleware_chain = middleware_chain()

        self.middleware = middleware_chain

        self.events = Events()
        self.strict_router_check = False

        self._request_class = request_class
        self._response_class = response_class

        self.handle_404 = self.default_404_handler
        self.log = logger.getChild("id=%x" % id(self))


    def all(self, path="/", middleware=None):
        pass

    def get(self, path="/", middleware=None):
        pass

    def post(self, path="/", middleware=None):
        pass

    def put(self, path="/", middleware=None):
        pass

    def delete(self, path="/", middleware=None):
        pass

    def use(self, middleware=None, path='/', method_mask=HTTPMethod.ALL):
        pass

    def add_router(self, path, router):
        pass

    @property
    def router(self):
        pass

    @property
    def has_root_router(self):
        pass

    async def handle_client_request(self, req, res):
        pass

    async def handle_server_error(self,
                                  req,
                                  res,
                                  mw_generator,
                                  error,
                                  err_count=0):
        pass

    def handle_response_not_sent(self, req, res):
        pass

    def print_middleware_tree(self,
                              *,
                              EOL=os.linesep,
                              **kwargs):  # noqa pragma: no cover
        pass

    @staticmethod
    def default_error_handler(req, res, error: Exception):
        pass

    @staticmethod
    def default_404_handler(req, res, error=None):
        pass


    def enable(self, name):
        pass

    def disable(self, name):
        pass

    def enabled(self, name):
        pass


    def __setitem__(self, key, value):
        """Sets a member of the application's configuration."""
        self.config[key] = value
        return value

    def __getitem__(self, key):
        """Gets a member of the application's configuration."""
        return self.config[key]

    def __delitem__(self, key):
        """Deletes a configuration parameter from the web-app"""
        del self.config[key]

    def __contains__(self, key):
        """Returns whether a key is in the application configuration."""
        return self.config.__contains__(key)


    def create_server(self,
                      protocol_factory=None,
                      *,
                      loop=None,
                      as_coroutine=False,
                      **server_config):
        pass

    def create_server_and_run_forever(self, loop=None, **server_config):
        pass

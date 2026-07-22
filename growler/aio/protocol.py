
from typing import Callable

import asyncio
import logging
from growler.responder import GrowlerResponder, ResponderHandler

ResponderFactoryType = Callable[['GrowlerProtocol'], GrowlerResponder]

logger = logging.getLogger(__name__)


class GrowlerProtocol(asyncio.Protocol, ResponderHandler):
    def __init__(self, _loop, responder_factory: ResponderFactoryType):
        """
        Args:
            responder_factory (callable): Returns the first responder
                for this protocol.
                This could simply be a constructor for the type (i.e.
                the type's name).
                This function will only be passed the protocol object.
                The event loop should be aquired from the protocol via
                the 'loop' member.
                The responder returned only needs to have a method
                defined called 'on_data' which gets passed the bytes
                received.
                Note: 'on_data' should only be a function and NOT a
                coroutine.
        """
        from typing import List, Optional
        self.make_responder = responder_factory
        self.log = logger.getChild("id=%x" % id(self))
        self.responders: List[GrowlerResponder] = []
        self.transport = None
        self.is_done_transmitting = False

    def connection_made(self, transport: asyncio.BaseTransport):
        pass

    def connection_lost(self, exc):
        pass

    def data_received(self, data):
        pass

    def eof_received(self):
        pass

    def handle_error(self, error):
        """
        An error handling function which will be called when an error
        is raised during a responder's :method:`on_data()` function.
        There is no default functionality and all subclasses SHOULD
        overload this.

        Args:
            error (Exception): The exception raised from the code
        """
        raise NotImplementedError(error)

    @classmethod
    def factory(cls, *args, **kw):
        pass

    @classmethod
    def get_factory(cls, *args, **kw):
        pass

del Callable

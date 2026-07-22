
from typing import Optional
from asyncio import BaseTransport
from socket import socket as Socket

from abc import ABC, abstractmethod


class GrowlerResponder(ABC):
    @abstractmethod
    def on_data(self, data):
        raise NotImplementedError()


class CoroutineResponder(GrowlerResponder):
    def __init__(self, coro):
        self._coro = coro

    def on_data(self, data):
        pass



class ResponderHandler:

    __slots__ = (
        'transport',
    )

    transport: Optional[BaseTransport]

    @property
    def socket(self) -> Optional[Socket]:
        pass

    @property
    def peername(self):
        pass

    @property
    def cipher(self):
        pass

    @property
    def remote_hostname(self):
        pass

    @property
    def remote_port(self):
        pass


del ABC
del abstractmethod
del BaseTransport
del Optional
del Socket

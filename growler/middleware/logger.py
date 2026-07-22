
import logging
import asyncio


class Logger:

    DEFAULT = '/033[30m'
    RED     = '/033[31m'
    GREEN   = '/033[32m'
    YELLOW  = '/033[33m'
    BLUE    = '/033[34m'
    MAGENTA = '/033[35m'
    CYAN    = '/033[36m'
    WHITE   = '/033[37m'

    @classmethod
    def c(cls, color, msg):
        pass

    def __init__(self):
        pass

    def info(self, message):
        pass

    def warn(self, message):
        pass

    def error(self, message):
        pass

    def critical_error(self, message):
        pass

    def __call__(self, req, res):
        logging.info("Connection from {}".format(req.ip))
        req.log = self

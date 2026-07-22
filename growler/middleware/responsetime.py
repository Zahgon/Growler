
import time
import logging

logger = logging.getLogger(__name__)


class ResponseTime:

    UNIT_TO_FACTOR_MAP = {
        's': 1,
        'ms': 1000,
        'us': 1000000,
    }

    def __init__(self,
                 digits=3,
                 log=None,
                 units='ms',
                 header="X-Response-Time",
                 suffix=True,
                 clobber_header=False):
        """
        Construct ResponseTime middleware.

        Parameters:
            digits (int): precision
            log (Logger or None): Writes the time difference to the log
            units (str): Time units (default: milliseconds 'ms')
            header (str): Name of header to send response time as
            suffix (bool): Whether to format with
        """
        self.units = units
        self.header_name = header
        self.digits = digits
        self.log = log if log else logger.getChild("id=%x" % id(self))
        self.suffix = suffix
        self.clobber_header = clobber_header

    def __call__(self, req, res):
        start_time = time.monotonic()

        def on_header_send():
            pass

        res.events.on('before_headers', on_header_send)

    def format_timediff(self, td):
        pass

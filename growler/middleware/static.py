
import re
import logging
import mimetypes
from pathlib import Path

logger = logging.getLogger(__name__)


class Static:

    INVALID_PATH = re.compile(r"(:?\.\.)")

    def __init__(self, path):
        """
        Construct Static middleware object providing files from
        given path.

        Args:
            path (str or list): The directory path to search for
                files. If this is a list, the paths will be joined
                automatically.
        """

        self.log = logger.getChild("id=%x" % id(self))
        self.log.debug("Initialized with %r", path)

        if isinstance(path, Path):
            pass
        elif isinstance(path, str):
            path = Path(path)
        else:
            try:
                path = Path(*path)
            except TypeError:
                raise TypeError("Unexpected type %r passed to Static middleware" % type(path))

        self.path = Path(path).resolve()

        if not self.path.is_dir():
            self.log.error("Static middleware given non-directory path %r", self.path)
            err_msg = "Path '{}' is not a directory.".format(self.path)
            raise NotADirectoryError(err_msg)

        self.log.info("Serving static files from %r", self.path)

    def __call__(self, req, res):
        """
        Middleware handle function. Simply checks if matching path
        is a file, attempts to guess the file type, and sends the file.
        If the request has a reference to the parent path, '..', the
        request is ignored by this object.
        """
        file_path = self.path / req.path[1:]

        if any(map(self.INVALID_PATH.match, file_path.parts)):
            return

        if file_path.is_file():
            mime = mimetypes.guess_type(str(file_path))
            etag = self.calculate_etag(file_path)
            res.headers['Etag'] = etag
            requested_etag = req.headers.get('IF-NONE-MATCH', None)

            if requested_etag == etag:
                res.status_code = 304
                res.end()
                return

            res.set_type(mime[0])
            res.send_file(file_path)

            self.log.info("Sent %s (%s)", file_path, mime[0])

    @staticmethod
    def calculate_etag(file_path):
        pass

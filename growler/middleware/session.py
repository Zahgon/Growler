
import uuid
import logging
from abc import abstractmethod
from collections.abc import MutableMapping

logger = logging.getLogger(__name__)


class Session(MutableMapping):

    def __init__(self, storage, values=None):
        self._data = {} if values is None else values
        self._store = storage

    def __getitem__(self, name):
        return self._data[name]

    def __setitem__(self, name, value):
        self._data[name] = value

    def __delitem__(self, name):
        del self._data[name]

    def __len__(self):
        return self._data.__len__()



    def get(self, name, default=None):
        pass

    def __iter__(self):
        return self._data.__iter__()

    async def save(self):
        pass


class SessionStorage:

    @abstractmethod
    def save(self, sess):
        raise NotImplementedError


class DefaultSessionStorage(SessionStorage):

    def __init__(self, session_id_name='qid'):
        """
        Construct a session storage object using the parameter as the
        unique session key.
        """
        super().__init__()
        self.session_id_name = session_id_name
        self._sessions = {}
        self.log = logger.getChild("id=%x" % id(self))

    def __call__(self, req, res):
        """
        The middleware action. Adds a session member to the req object
        and the session id to the response object.
        """
        qid = self.session_id_name
        try:
            sid = req.cookies[qid].value
        except KeyError:
            sid = req.cookies[qid] = uuid.uuid4()

        res.cookies[qid] = sid

        self.log.debug("%r", sid)
        if sid not in self._sessions:
            self._sessions[sid] = {'id': sid}
        req.session = Session(self, self._sessions[sid])

    def save(self, sess):
        pass

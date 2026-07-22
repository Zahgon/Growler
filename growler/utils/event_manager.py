
from collections import defaultdict
from inspect import isawaitable


def event_emitter(cls_=None, *, events=('*', )):
    """
    A class-decorator which will add the specified events and the methods 'on'
    and 'emit' to the class.
    """

    event_dict = dict.fromkeys(events, [])

    allow_any_eventname = event_dict.pop('*', False) == []

    def _event_emitter(cls):

        def on(self, name, callback):
            pass

        async def emit(self, name):
            pass

        cls.on = on
        cls.emit = emit

        return cls

    if cls_ is None:
        return _event_emitter
    else:
        return _event_emitter(cls_)


def emits(pre=None, *, post=None):
    pass


class Events:

    def __init__(self, *event_names):
        """
        Construct Events object with a set of allowed event names.
        If no event names are given, then all events are allowed.


        """
        if ... in event_names or event_names == ():
            self._event_list = defaultdict(list)
        else:
            self._event_list = {name: [] for name in event_names}

    def on(self, name, _callback=None):
        pass

    async def emit(self, name):
        pass

    def sync_emit(self, name):
        pass

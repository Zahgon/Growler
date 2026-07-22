
import re
import logging
from inspect import signature
from collections import OrderedDict
from growler.http import HTTPMethod

ROUTABLE_NAME_REGEX = re.compile(
    "(%s)_.*" % '|'.join([
        "all",
        "get",
        "post",
        "put",
        "delete",
    ]), re.IGNORECASE + re.UNICODE)

logger = logging.getLogger(__name__)


class MiddlewareNode:

    IGNORE_TRAILING_SLASH = True

    __slots__ = [
        'func',
        'path',
        'mask',
        'is_errorhandler',
        'is_subchain',
    ]

    def __init__(self, **inits):
        """
        The path attribute should be a regular expression.
        If it is a string, it is escaped and then compiled.

        Keyword Args:
            path (String or regex): A regex to be matched upon
                connection Simple mappings to attributes
        """
        for k, v in inits.items():
            if k == 'path' and isinstance(v, str):
                v = self.path_to_regex(v)
            setattr(self, k, v)

    @staticmethod
    def path_to_regex(path):
        pass

    def matches_method(self, method):
        pass

    def path_split(self, path):
        pass


class MiddlewareChain:

    ROOT_PATTERN = re.compile(re.escape('/'))

    def __init__(self):
        self.mw_list = []
        self.log = logging.getLogger("%s:%d" % (__name__, id(self)))

    def __call__(self, method, path):
        """
        Generator yielding the middleware which matches the provided path.

        When called with an HTTP method and path, the middleware
        chain returns a generator object that will walk along the
        chain in a depth-first pattern. Any middleware nodes
        matching both the method code and path are yielded.

        The generator keeps any error handlers encountered walking
        the tree in its internal state. If an error occurs during
        execution of a middleware function, the exception should be
        sent back to the generator via the throw method:
        ``mw_chain.throw(err)``.
        The error handlers will be looped through in reverse order,
        so the most specific handler matching method and path is
        called first.

        If an error occurs during the execution of an error handler,
        it is ignored (for now) until a solution is determined.

        Args:
            method (growler.http.HTTPMethod): The request method which
            path (str): URL path of the request.

        Yields:
            Callable or Coroutine: The next middleware object that
            matches the incoming request

        TODO:
            What to do when the error handler raises a new error?
        """
        error_handler_stack = []

        matching_middleware = self.find_matching_middleware(method, path)
        for mw, path_match, rest_url in matching_middleware:

            if mw.is_subchain:

                subpath = '/' + rest_url

                subchain = mw.func(method, subpath)

                yield from self.iterate_subchain(subchain)

            elif mw.is_errorhandler:
                error_handler_stack.append(mw.func)

            else:
                try:
                    yield mw.func

                except Exception as err:
                    yield None
                    yield from self.handle_error(err, error_handler_stack)
                    break

    def find_matching_middleware(self, method, path):
        pass

    def iterate_subchain(self, chain):
        pass

    def handle_error(self, error, err_handlers):
        pass

    def should_skip_middleware(self, middleware, matching, rest):
        pass

    def add(self, method_mask, path, func):
        pass

    def __contains__(self, func):
        """
        Returns whether the function is stored anywhere in the
        middleware chain.

        This runs recursively though any subchains.

        Args:
            func (callable): A function which may be present in the
                chain

        Returns:
            bool: True if func is a function contained anywhere in
                the chain.
        """
        return any((func is mw.func) or (mw.is_subchain and func in mw.func)
                   for mw in self.mw_list)

    def count_all(self):
        pass

    def __len__(self):
        """
        Returns the number of middleware contained in the root of
        this chain.
        To count the number of middleware, included in subchains, use
        count_all().
        """
        return len(self.mw_list)

    def __iter__(self):
        """
        Iterates directly through the middleware chain. Does not
        enter any subchains.
        """
        return iter(self.mw_list)

    def __reversed__(self):
        """
        Iterates directly through the middleware chain, starting
        from the bottom.
        Does not enter any subchains along the way.
        """
        return reversed(self.mw_list)

    def first(self):
        pass

    def last(self):
        pass


class Router(MiddlewareChain):
    sinatra_param_regex = re.compile(r":(\w+)")
    regex_type = type(sinatra_param_regex)

    def __init__(self):
        super().__init__()
        self.log = logger.getChild("id=%x" % id(self))
        self.add_route = self.add

    def add_router(self, path, router):
        pass

    def _add_route(self, method, path, middleware=None):
        pass

    def all(self, path, middleware=None):
        pass

    def get(self, path, middleware=None):
        pass

    def post(self, path, middleware=None):
        pass

    def put(self, path, middleware=None):
        pass

    def delete(self, path, middleware=None):
        pass

    def use(self, middleware, path=None):
        pass

    def match_routes(self, req):
        pass

    def iter_routes(self):
        pass

    def should_skip_middleware(self, middleware, matching, rest) -> bool:
        pass

    @property
    def routes(self):
        pass

    @property
    def subrouters(self):
        pass

    @classmethod
    def sinatra_path_to_regex(cls, path):
        pass


class RouterMeta(type):
    @classmethod
    def __prepare__(metacls, name, bases, **kargs):
        """
        Metaclass attribute which creates the mapping object - in
        this case a standard :class:`collections.OrderedDict` object
        to preserve order of method names.

        Args:
            name (str): The name of the class
            base (tuple): Collection of baseclasses
        Return:
            Simple ordered dict to store the class members/methods
        """
        return OrderedDict()

    def __new__(cls, name, bases, classdict):
        """
        Creates the class type, adding an additional attributes
        __ordered_attrs__, a snapshot of the dictionary keys, and
        __growler_router, a method which will generate a growler.Router
        object.
        """
        child_class = type.__new__(cls, name, bases, classdict)

        def build_router(self):
            pass

        child_class.__growler_router = build_router
        return child_class


def _find_routeable_attributes(obj, keys):
    """
    From the set of provided `keys`, this function yields the attributes
    of `obj` that fulfill the requirements of 'routeable':
    * callable
    * matched by ROUTABLE_NAME_REGEX
    * has docstring

    """
    for attr in keys:
        matches = ROUTABLE_NAME_REGEX.match(attr)
        if matches is None:
            continue
        try:
            val = getattr(obj, attr)
        except AttributeError:
            continue

        if not callable(val) or val.__doc__ is None:
            continue

        method_name = matches.group(1).upper()
        yield val, method_name


def get_routing_attributes(obj, modify_doc=False, keys=None):
    """
    Loops through the provided object (using the dir() function) and
    finds any callables which match the name signature (e.g.
    get_foo()) AND has a docstring beginning with a path-like char
    string.
    This does process things in alphabetical order (rather than than
    the unpredictable __dict__ attribute) so take this into
    consideration if certain routes should be checked before others.
    Unfortunately, this is a problem because the 'all' method will
    always come before others, so there is no capturing one type
    followed by a catch-all 'all'. Until a solution is found, just
    make a router by hand.
    """
    if keys is None:
        keys = dir(obj)

    for val, method_str in _find_routeable_attributes(obj, keys):

        path, *doc = val.__doc__.split(maxsplit=1) or ('', '')

        if not path:
            continue

        if modify_doc:
            val.__doc__ = ''.join(doc)

        method = HTTPMethod[method_str]

        yield method, path, val


def routerclass(cls):
    pass


def routerify(obj):
    pass

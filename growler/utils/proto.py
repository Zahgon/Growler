
from collections import namedtuple


BoundFunction = namedtuple("BoundFunction", 'func')


class PrototypeMeta(type):
    pass


class PrototypeObject(metaclass=PrototypeMeta):

    __proto__ = object()
    __methods__ = None

    @classmethod
    def create(cls, obj):
        pass

    def bind(self, func):
        pass

    def has_own_property(self, attr):
        pass

    def __getattr__(self, attr):
        """
        Called by python when an attribute is not found.
        This will call the __getprotoattr__ to search the chain.

        If a BoundFunction is found, it gets bound to 'self' and the
        resulting method is returned.
        """
        result = self.__getprotoattr__(attr)
        if isinstance(result, BoundFunction):
            result = result.func.__get__(self)
        return result

    def __getprotoattr__(self, attr):
        """
        Recursively search through object's prototype-chain,
        """
        if self.__methods__ and attr in self.__methods__:
            return self.__methods__[attr]

        try:
            return object.__getattribute__(self.__proto__, attr)
        except AttributeError:
            pass

        try:
            return self.__proto__.__getprotoattr__(attr)
        except AttributeError:
            raise AttributeError("{!r} object has no attribute {!r}".format(
                self.__class__.__name__,
                attr))

    def __setattr__(self, attr, value):
        if self.__methods__ and attr in self.__methods__:
            del self.__methods__[attr]
        object.__setattr__(self, attr, value)

    def __delattr__(self, attr):
        """
        Remove the attribute from this object.
        If attribute exists in prototype, this has no effect.

        The __proto__ and __methods__ attributes are protected
        and must not be deleted.
        """
        if attr in ('__proto__', '__methods__'):
            raise RuntimeError(
                "Attempted to delete {} from PrototypeObject".format(attr)
            )

        try:
            object.__delattr__(self, attr)
        except AttributeError:
            if not hasattr(self.__proto__, attr):
                raise

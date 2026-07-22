

class ItemizedMeta(type):

    def __getitem__(cls, key):
        return cls._getitem_(key)

    def __setitem__(cls, key, val):
        return cls._setitem_(key, val)

    def __delitem__(cls, key):
        return cls._delitem_(key)

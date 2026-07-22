
import enum


class HTTPMethod(enum.IntEnum):
    ALL    = 0b011111
    GET    = 0b000001
    POST   = 0b000010
    DELETE = 0b000100
    PUT    = 0b001000
    HEAD   = 0b010000

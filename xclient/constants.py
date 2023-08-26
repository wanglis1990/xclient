from enum import Enum, unique


@unique
class XStatusCode(Enum):
    """响应码"""

    SUCCESS = 200

    CREATED = 201

    UNAUTHORIZED = 401

    FORBIDDEN = 403

    NOTFOUND = 404


@unique
class XErrCode(Enum):
    pass

from enum import IntEnum


class BusinessResponseCode(IntEnum):
    """
    业务通用返回代码
    """

    SUCCESS = 0
    FAILED = 1

    USER_NOT_FOUND = 1001
    USER_ALREADY_EXISTS = 1002
    USER_PASSWORD_ERROR = 1003
    USER_NOT_ACTIVE = 1004
    USER_NOT_SUPERUSER = 1005
    USER_NOT_LOGIN = 1006
    USER_LOGIN_FAILED = 1007

from enum import Enum


class AuthType(Enum):
    NONE = "NONE"
    TRADE = "TRADE"
    USER_DATA = "USER_DATA"
    USER_STREAM = "USER_STREAM"
    MARKET_DATA = "MARKET_DATA"

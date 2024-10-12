import json
from binance_sdk.consts import *
from binance_sdk.async_client import AsyncClient
from binance_sdk.util.http_method import Method
from binance_sdk.util.auth_type import AuthType


class AsyncInvertDerivApi(AsyncClient):

    def __init__(self, api_key: str, secret_key: str):
        super().__init__(api_key, secret_key, COIN_M_URL)

    async def get_account(self, should_log=True):
        return await self.request(
            method=Method.GET,
            request_path=REST_INVERT_ACCT_POS,
            auth_type=AuthType.USER_DATA,
            should_log=should_log,
        )

    async def set_leverage(self, symbol: str, leverage: int, should_log=True):
        params = {"symbol": symbol, "leverage": leverage}
        return await self.request(
            method=Method.POST,
            request_path=REST_INVERT_LEVERAGE,
            params=params,
            auth_type=AuthType.TRADE,
            should_log=should_log,
        )

    async def get_exchange_info(self, should_log=True):
        return await self.request(
            method=Method.GET,
            request_path=REST_ALL_INVERT_DERIV_INST,
            should_log=should_log,
        )

    async def get_open_orders(self, symbol: str=None, should_log=True):
        params = {"symbol": symbol} if symbol else {}
        return await self.request(
            method=Method.GET,
            request_path=REST_INVERT_OPEN_ORDERS,
            params=params,
            auth_type=AuthType.USER_DATA,
            should_log=should_log,
        )

    async def get_position_mode(self, should_log=True):
        return await self.request(
            method=Method.GET,
            request_path=REST_INVERT_POSN_MODE,
            auth_type=AuthType.USER_DATA,
            should_log=should_log,
        )

    async def set_position_mode(self, dual_side_position: bool, should_log=True):
        params = {"dualSidePosition": json.dumps(dual_side_position)}
        return await self.request(
            method=Method.POST,
            request_path=REST_INVERT_POSN_MODE,
            params=params,
            auth_type=AuthType.TRADE,
            should_log=should_log,
        )

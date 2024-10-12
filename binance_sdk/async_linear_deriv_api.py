import json
import pandas as pd
from binance_sdk.consts import *
from binance_sdk.async_client import AsyncClient
from binance_sdk.util.http_method import Method
from binance_sdk.util.auth_type import AuthType


class AsyncLinearDerivApi(AsyncClient):

    def __init__(self, api_key: str, secret_key: str):
        super().__init__(api_key, secret_key, USDT_M_URL)

    async def get_account(self, should_log=True):
        return await self.request(
            method=Method.GET,
            request_path=REST_LINEAR_ACCOUNT,
            auth_type=AuthType.USER_DATA,
            should_log=should_log,
        )
    
    async def get_positions(self, symbol: str=None, should_log=True):
        params = {"symbol": symbol} if symbol else {}
        return await self.request(
            method=Method.GET,
            request_path=REST_LINEAR_POSN_RISK_V3,
            params=params,
            auth_type=AuthType.TRADE,
            should_log=should_log,
        )

    async def close_positions(self, symbol: str=None, should_log=True) -> dict:
        result = dict()
        positions = await self.get_positions(symbol=symbol, should_log=should_log)
        for position in positions:
            symbol = position["symbol"]
            position_amt = float(position["positionAmt"])
            side = "BUY" if position_amt < 0 else "SELL"
            resp = await self.new_order(symbol, side, "MARKET", quantity=abs(position_amt), should_log=should_log)
            result[symbol] = resp
        return result

    async def new_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        position_side: str = None,
        time_in_force: str = None,
        quantity: float = None,
        reduce_only: bool = None,
        price: float = None,
        new_client_order_id: str = None,
        stop_price: float = None,
        close_position: bool = None,
        activation_price: float = None,
        callback_rate: float = None,
        working_type: str = None,
        price_protect: str = None,
        new_order_resp_type: str = None,
        price_match: str = None,
        self_trade_prevention_mode: str = None,
        good_till_date: int = None,
        is_test: bool = False,
        should_log=True,
    ):
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "positionSide": position_side,
            "timeInForce": time_in_force,
            "quantity": quantity,
            "reduceOnly": json.dumps(reduce_only) if reduce_only is not None else None,
            "price": price,
            "newClientOrderId": new_client_order_id,
            "stopPrice": stop_price,
            "closePosition": json.dumps(close_position) if close_position is not None else None, 
            "activationPrice": activation_price,
            "callbackRate": callback_rate,
            "workingType": working_type,
            "priceProtect": price_protect,
            "newOrderRespType": new_order_resp_type,
            "priceMatch": price_match,
            "selfTradePreventionMode": self_trade_prevention_mode,
            "goodTillDate": good_till_date,
        }
        params = {k: v for k, v in params.items() if v is not None}
        request_path = REST_LINEAR_ORDER_TEST if is_test else REST_LINEAR_ORDER
        return await self.request(method=Method.POST, request_path=request_path, params=params, auth_type=AuthType.TRADE, should_log=should_log)

    async def get_klines(self, symbol: str, interval: str, start_time: int=None, end_time: int=None, time_zone: str=None, limit: int=None, should_log=True):
        params = {"symbol": symbol, "interval": interval, "startTime": start_time, "endTime": end_time, "timeZone": time_zone, "limit": limit}
        params = {k: v for k, v in params.items() if v is not None}
        return await self.request(method=Method.GET, request_path=REST_LINEAR_KLINES, params=params, should_log=should_log)

    async def get_klines_df(self, symbol: str, interval: str, start_time: int=None, end_time: int=None, time_zone: str=None, limit: int=None, should_log=True) -> pd.DataFrame:
        data = await self.get_klines(symbol, interval, start_time=start_time, end_time=end_time, time_zone=time_zone, limit=limit, should_log=should_log)
        df = pd.DataFrame(data, columns=["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_asset_volume", "number_of_trades", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "unused_field"])
        df = df[["open_time", "open", "high", "low", "close"]]
        for col in ["open", "high", "low", "close"]: df[col] = df[col].map(float)
        return df

    async def get_price(self, symbol: str, should_log=True):
        params = {"symbol": symbol}
        return await self.request(
            method=Method.GET,
            request_path=REST_LINEAR_TICKER_PRICE,
            params=params,
            should_log=should_log,
        )

    async def set_leverage(self, symbol: str, leverage: int, should_log=True):
        params = {"symbol": symbol, "leverage": leverage}
        return await self.request(
            method=Method.POST,
            request_path=REST_LINEAR_LEVERAGE,
            params=params,
            auth_type=AuthType.TRADE,
            should_log=should_log,
        )
    
    async def get_symbol_config(self, symbol: str=None, should_log=True):
        params = {"symbol": symbol} if symbol else {}
        return await self.request(
            method=Method.GET,
            request_path=REST_LINEAR_SYMBOL_CONFIG,
            params=params,
            auth_type=AuthType.USER_DATA,
            should_log=should_log,
        )

    async def get_exchange_info(self, should_log=True):
        return await self.request(
            method=Method.GET,
            request_path=REST_ALL_LINEAR_DERIV_INST,
            should_log=should_log,
        )

    async def get_open_orders(self, symbol: str=None, should_log=True):
        params = {"symbol": symbol} if symbol else {}
        return await self.request(
            method=Method.GET,
            request_path=REST_LINEAR_OPEN_ORDERS,
            params=params,
            auth_type=AuthType.USER_DATA,
            should_log=should_log,
        )

    async def get_position_mode(self, should_log=True):
        return await self.request(
            method=Method.GET,
            request_path=REST_LINEAR_POSN_MODE,
            auth_type=AuthType.USER_DATA,
            should_log=should_log,
        )

    async def set_position_mode(self, dual_side_position: bool, should_log=True):
        params = {"dualSidePosition": json.dumps(dual_side_position)}
        return await self.request(
            method=Method.POST,
            request_path=REST_LINEAR_POSN_MODE,
            params=params,
            auth_type=AuthType.TRADE,
            should_log=should_log,
        )

    async def get_user_trades(
        self,
        symbol: str,
        order_id: int=None,
        start_time: int=None,
        end_time: int=None,
        from_id: int=None,
        limit: int=None,
        should_log=True
    ):
        params = {
            "symbol": symbol,
            "orderId": order_id,
            "startTime": start_time,
            "endTime": end_time,
            "fromId": from_id,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        return await self.request(
            method=Method.GET,
            request_path=REST_LINEAR_USER_TRADES,
            params=params,
            auth_type=AuthType.USER_DATA,
            should_log=should_log,
        )

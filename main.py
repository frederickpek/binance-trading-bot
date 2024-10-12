import asyncio
import pandas as pd
from signals import *
from typing import Dict, List
from util.logs import logging
from binance_sdk.async_linear_deriv_api import AsyncLinearDerivApi
from secret import BINANCE_API_KEY, BINANCE_SECRET_KEY


class BinanceFapiCrudeV3:

    def __init__(
        self,
        symbol: str,
        default_qty: int,
        fapi: AsyncLinearDerivApi,
        interval: str = "5m",
        sma_length: int = 70,
        dist_sma: float = 0.014,
        leverage: int = 8,
        tick_period_sec: float = 10,
        close_all_positions_on_start=True,
    ):
        self.symbol = symbol
        self.default_qty = default_qty
        self.fapi = fapi
        self.interval = interval
        self.sma_length = sma_length
        self.dist_sma = dist_sma
        self.leverage = leverage

        # configs
        self.tick_period_sec = tick_period_sec
        self.close_all_positions_on_start = close_all_positions_on_start

        # current signals
        self.df: pd.DataFrame = None

        # position states
        self.in_buy_position = False
        self.last_buy_open_time: int = 0

        self.in_sell_position = False
        self.last_sell_open_time: int = 0

    async def get_crude_v3_signals(self) -> pd.DataFrame:
        df = await self.fapi.get_klines_df(self.symbol, self.interval, limit=100, should_log=False)
        df = crude_v3(df, sma_length=self.sma_length, dist_sma=self.dist_sma)
        return df

    def buy(self, df: pd.DataFrame=None) -> bool:
        df = df or self.df
        if self.in_buy_position:
            # already in buy position, ignore signal
            return False
        if self.last_buy_open_time == df.iloc[-2]["open_time"]:
            # already bought for this candle, ignore signal
            return False
        if df.iloc[-1]["close"] >= df.iloc[-1][GAPS]:
            # will TP next tick, shouldn't enter
            return False
        # use previous candle
        return df.iloc[-2][BUY]

    def sell(self, df: pd.DataFrame=None) -> bool:
        df = df or self.df
        if self.in_sell_position:
            # already in sell position, ignore signal
            return False
        if self.last_sell_open_time == df.iloc[-2]["open_time"]:
            # already sold for this candle, ignore signal
            return False
        if df.iloc[-1]["close"] <= df.iloc[-1][GAPB]:
            # will TP next tick, shouldn't enter
            return False
        # use previous candle
        return df.iloc[-2][SELL]

    def close_buy_take_profit(self, df: pd.DataFrame=None) -> bool:
        df = df or self.df
        return self.in_buy_position and df.iloc[-1]["close"] >= df.iloc[-1][GAPS]

    def close_sell_take_profit(self, df: pd.DataFrame=None) -> bool:
        df = df or self.df
        return self.in_sell_position and df.iloc[-1]["close"] <= df.iloc[-1][GAPB]

    def close_buy_stop_loss(self, df: pd.DataFrame=None) -> bool:
        df = df or self.df
        return self.in_buy_position and df.iloc[-1]["close"] <= df.iloc[-1][GAPB]

    def close_sell_stop_loss(self, df: pd.DataFrame=None) -> bool:
        df = df or self.df
        return self.in_sell_position and df.iloc[-1]["close"] >= df.iloc[-1][GAPS]

    async def update_signals(self, should_log=True):
        try:
            crude_v3_signals = await self.get_crude_v3_signals()
            self.df = crude_v3_signals
            if should_log:
                logging.info(f"{self.symbol} signals updated\n{crude_v3_signals.tail(n=1).to_string()}")
        except Exception as err:
            logging.exception(f"{self.symbol} failed to update signals")
            raise err

    async def get_symbol_position(self) -> dict:
        resp = await self.fapi.get_account()
        positions = resp["positions"]
        for position in positions:
            if position["symbol"] != self.symbol:
                continue
            return position
        return dict()

    def get_theoretical_position_amount(self) -> int:
        if self.in_buy_position:
            return self.default_qty
        if self.in_sell_position:
            return -self.default_qty
        return 0

    async def process_buy_order(self):
        buy_qty = self.default_qty - self.get_theoretical_position_amount()
        if buy_qty <= 0:
            logging.info(f"{self.symbol} position already exists, ignoring buy order")
            return
        resp = await self.fapi.new_order(self.symbol, "BUY", "MARKET", quantity=buy_qty)
        logging.info(f"{self.symbol} BUY Order Placed: {resp}")

    async def process_sell_order(self):
        sell_qty = self.default_qty + self.get_theoretical_position_amount()
        if sell_qty <= 0:
            logging.info(f"{self.symbol} position already exists, ignoring sell order")
            return
        resp = await self.fapi.new_order(self.symbol, "SELL", "MARKET", quantity=sell_qty)
        logging.info(f"{self.symbol} SELL Order Placed: {resp}")

    async def close_all_positions(self, posn_amt: int=None):
        if not posn_amt:
            tpa = self.get_theoretical_position_amount()
            if not tpa:
                logging.info(f"{self.symbol} no positions to close, close ignoring order")
                return
            posn_amt = tpa
        side = "BUY" if posn_amt < 0 else "SELL"
        resp = await self.fapi.new_order(self.symbol, side, "MARKET", quantity=int(abs(posn_amt)))
        logging.info(f"{self.symbol} Closed all positions with {side} Order: {resp}")

    def update_position_status(self, in_buy_position=False, in_sell_position=False, df: pd.DataFrame=None):
        df = df or self.df
        if not self.in_buy_position and in_buy_position:
            self.last_buy_open_time = df.iloc[-2]["open_time"]
        if not self.in_sell_position and in_sell_position:
            self.last_sell_open_time = df.iloc[-2]["open_time"]
        self.in_buy_position = in_buy_position
        self.in_sell_position = in_sell_position

    async def process_tick(self):
        await self.update_signals(should_log=False)

        if self.buy():
            logging.info(f"{self.symbol} BUY signal detected, executing buy order", send_lark=True)
            await self.process_buy_order()
            self.update_position_status(in_buy_position=True)
        elif self.sell():
            logging.info(f"{self.symbol} SELL signal detected, executing sell order", send_lark=True)
            await self.process_sell_order()
            self.update_position_status(in_sell_position=True)
        elif self.close_buy_take_profit():
            logging.info(f"{self.symbol} CBTP signal detected, closing positions", send_lark=True)
            await self.close_all_positions()
            self.update_position_status()
        elif self.close_sell_take_profit():
            logging.info(f"{self.symbol} CSTP signal detected, closing positions", send_lark=True)
            await self.close_all_positions()
            self.update_position_status()
        elif self.close_buy_stop_loss():
            logging.info(f"{self.symbol} CBSL signal detected, closing positions", send_lark=True)
            await self.close_all_positions()
            self.update_position_status()
        elif self.close_sell_stop_loss():
            logging.info(f"{self.symbol} CSSL signal detected, closing positions", send_lark=True)
            await self.close_all_positions()
            self.update_position_status()

    async def set_symbol_leverage(self):
        resp = await self.fapi.set_leverage(self.symbol, self.leverage)
        logging.info(f"{self.symbol} leverage set: {resp}")
        
    async def ensure_no_open_positions(self):
        posn = await self.get_symbol_position()
        posn_amt = float(posn.get("positionAmt", 0))
        if not posn_amt:
            return
        if self.close_all_positions_on_start:
            await self.close_all_positions(posn_amt=posn_amt)
            logging.info(f"{self.symbol} positions closed")
            return
        raise Exception(f"Open position detected: {posn}")

    async def setup(self):
        self.update_position_status()
        await asyncio.gather(self.ensure_no_open_positions(), self.set_symbol_leverage())
        params = {
            "Strategy Name": self.__class__.__name__,
            "Symbol": self.symbol,
            "Interval": self.interval,
            "Default Quantity": self.default_qty,
            "SMA Length": self.sma_length,
            "Dist SMA": self.dist_sma,
            "Leverage": self.leverage,
        }
        logging.info(f"{self.symbol} setup complete\n{pd.Series(params).to_string(dtype=False)}")

    async def fail_safe_close_all_positions(self):
        result = await self.fapi.close_positions()
        if result:
            logging.info(f"{self.symbol} fail-safe close all position {result=}", send_lark=True)

    def get_progress(self) -> float:
        """
        Returns the progress as a percentage from TP/SL point
        """
        if not self.in_buy_position and not self.in_sell_position:
            return 0
        if self.df is None or self.df.empty:
            return 0
        close = self.df.iloc[-1]["close"]
        sma = self.df.iloc[-1][SMA]
        gaps = self.df.iloc[-1][GAPS]
        gapb = self.df.iloc[-1][GAPB]
        if close > sma:
            return (close - sma) / (gaps - sma) * (-1 if self.in_sell_position else 1)
        elif close < sma:
            return (sma - close) / (sma - gapb) * (-1 if self.in_buy_position else 1)
        return 0

    async def run(self):
        await self.setup()
        contiguous_error_cycles = 0
        while True:
            try:
                initial_posn = self.get_theoretical_position_amount()
                await self.process_tick()
                final_posn = self.get_theoretical_position_amount()
                if initial_posn == final_posn:
                    posn_update = f"{final_posn=:,}"
                else:
                    posn_update = f"{initial_posn=:,} -> {final_posn=:,}"
                logging.info(f"{self.symbol} tick processed, {posn_update}, sleeping for {self.tick_period_sec}s")
                await asyncio.sleep(self.tick_period_sec)
                contiguous_error_cycles = 0
            except Exception:
                contiguous_error_cycles += 1
                logging.exception(f"{self.symbol} error processing tick", send_lark=True)
                await asyncio.sleep(60)
            if contiguous_error_cycles >= 10:
                break
        logging.info(f"{self.symbol} {contiguous_error_cycles=}, stopping strategy", send_lark=True)
        try:
            await self.fail_safe_close_all_positions()
        except Exception:
            logging.exception(f"{self.symbol} attempt at closing all positions failed", send_lark=True)
        return


class BinanceFapiCrudeV3StrategyManager:
    def __init__(self, fapi: AsyncLinearDerivApi):
        self.fapi = fapi
        self.strategies: Dict[str, BinanceFapiCrudeV3] = dict()

    def add_strategies(self, params_list: List[dict]):
        for params in params_list:
            self.add_strategy_with_dict(params=params)

    def add_strategy_with_dict(self, params: dict):
        symbol = params.get("symbol")
        if not symbol:
            raise ValueError("no symbol")
        if symbol in self.strategies:
            raise ValueError(f"duplicate {symbol=} found")
        self.strategies[symbol] = BinanceFapiCrudeV3(fapi=self.fapi, **params)

    async def run_strategies(self):
        await asyncio.gather(*[strat.run() for strat in self.strategies.values()])

    async def log_portfolio_status(self):
        while True:
            try:
                _fn = lambda x: f"${float(x):,.3f}" if float(x) > 1 else f"${float(x):.3g}"
                positions = await fapi.get_positions()
                if positions:
                    df = pd.DataFrame(positions)
                    df["qty"] = df["positionAmt"].map(lambda x: float(x))
                    df["side"] = df["qty"].map(lambda x: "LONG" if x > 0 else "SHORT" if x < 0 else "")
                    df["qty"] = df["qty"].abs()
                    df["entry"] = df["entryPrice"].map(_fn)
                    df["mark"] = df["markPrice"].map(_fn)
                    df["liq"] = df["liquidationPrice"].map(_fn)
                    df["upl"] = df["unRealizedProfit"].map(lambda x: f"${float(x):,.2f}")
                    df["notional"] = df["notional"].map(lambda x: f"${abs(float(x)):,.2f}")
                    df["interval"] = df["symbol"].map(lambda x: self.strategies[x].interval)
                    df["dist_sma"] = df["symbol"].map(lambda x: self.strategies[x].dist_sma)
                    df["progress"] = df["symbol"].map(lambda x: f"{self.strategies[x].get_progress() * 100:.2f}%")
                    df = df[["symbol", "side", "qty", "notional", "entry", "mark", "liq", "upl", "interval", "dist_sma", "progress"]]
                    logging.info(f"Portfolio Status\n{df.to_string(index=False)}")
            except Exception:
                logging.exception("Error retreiving account positions")
            await asyncio.sleep(60)

    async def send_heartbeat(self):
        while True:
            try:
                logging.info(f"{self.__class__.__name__} heartbeat", send_lark=True)
            except Exception:
                logging.exception("Error retreiving account positions")
            await asyncio.sleep(600)

    async def main(self):
        await asyncio.gather(
            asyncio.create_task(self.run_strategies()),
            asyncio.create_task(self.log_portfolio_status()),
            asyncio.create_task(self.send_heartbeat()),
        )


if __name__ == "__main__":
    symbol_params = [
        {"symbol": "JUPUSDT", "default_qty": 5_000, "interval": "5m", "dist_sma": 0.014},
        {"symbol": "SOLUSDT", "default_qty": 20, "interval": "5m", "dist_sma": 0.014},
        {"symbol": "DOGSUSDT", "default_qty": 2_000_000, "interval": "5m", "dist_sma": 0.014},
        {"symbol": "WIFUSDT", "default_qty": 1_500, "interval": "5m", "dist_sma": 0.014},
        {"symbol": "PYTHUSDT", "default_qty": 10_000, "interval": "5m", "dist_sma": 0.014},
    ]
    fapi = AsyncLinearDerivApi(BINANCE_API_KEY, BINANCE_SECRET_KEY)
    strategy_manager = BinanceFapiCrudeV3StrategyManager(fapi)
    strategy_manager.add_strategies(symbol_params)
    asyncio.run(strategy_manager.main())

import numpy as np
import pandas as pd
import pandas_ta as ta

SMA = "SMA"
BUY = "BUY"
SELL = "SELL"
GAPS = "GAPS"
GAPB = "GAPB"
GAPS_HALF = "GAPSHALF"
GAPB_HALF = "GAPBHALF"

def crude_signal(df: pd.DataFrame, sma_length: int=70) -> pd.DataFrame:
    df[SMA] = df.ta.sma(length=sma_length)
    df[BUY] = ta.cross(df['close'].shift(1), df[SMA]) & (df['close'].shift(1) > df['open'].shift(1)) & (df['high'] > df['high'].shift(1)) & (df['close'] > df['open'])
    df[SELL] = ta.cross(df['close'].shift(1), df[SMA], above=False) & (df['close'].shift(1) < df['open'].shift(1)) & (df['low'] < df['low'].shift(1)) & (df['close'] < df['open'])
    return df

def crude_v2(df: pd.DataFrame, sma_length: int=70, dist_sma: float=0.022):
    """
    =====================   SMA * (1 + dist_sma)            GAPS

    - -- - -- - -- - -- -   SMA * (1 + dist_sma / 2)        GAPS_HALF

    ---------------------   SMA                             BUY/SELL Signal

    - -- - -- - -- - -- -   SMA / (1 + dist_sma / 2)        GAPB_HALF

    =====================   SMA / (1 + dist_sma)            GAPB
    """
    df = crude_signal(df, sma_length=sma_length)
    df[GAPS] = df[SMA] * (1 + dist_sma)
    df[GAPB] = df[SMA] / (1 + dist_sma)
    df[GAPS_HALF] = df[SMA] * (1 + dist_sma / 2)
    df[GAPB_HALF] = df[SMA] / (1 + dist_sma / 2)
    return df

def crude_v3(df: pd.DataFrame, sma_length: int=70, dist_sma: float=0.014):
    """
    =====================   SMA * (1 + dist_sma)            GAPS

    ---------------------   SMA                             BUY/SELL Signal

    =====================   SMA / (1 + dist_sma)            GAPB
    """
    df = crude_signal(df, sma_length=sma_length)
    df[GAPS] = df[SMA] * (1 + dist_sma)
    df[GAPB] = df[SMA] / (1 + dist_sma)
    return df

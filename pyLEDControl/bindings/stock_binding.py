from datetime import datetime, timedelta
from tkinter import CURRENT
from typing import Optional, TypedDict, cast
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from misc.logging import Log
import settings
import yfinance as yf
from diskcache import Cache
import pandas as pd

log = Log("StockBinding")


class StockData(TypedDict):
    """
        TypedDict for stock performance of a single symbol.
        All procentual values are floats.
    """
    symbol: str
    name: Optional[str]
    currency: Optional[str]
    last_updated: datetime

    # Latest Close-Preis
    close_current: float

    # Daily change
    change_1d_abs: float
    change_1d_pct: float

    # last 7 days
    change_7d_abs: float
    change_7d_pct: float

    # last 14 days
    change_14d_abs: float
    change_14d_pct: float

    # last month
    change_1m_abs: float
    change_1m_pct: float

    # last 6m
    change_6m_abs: float
    change_6m_pct: float


CURRENCIES = {
    "eur": "€",
    "usd": "$",
    "gbp": "£",
    "jpy": "¥",
    "chf": "CHF",
}


def map_currency_to_symbol(curr: str) -> str:
    if curr is None:
        return "$"
    return CURRENCIES.get(curr.lower(), "$")


class StockBinding:
    CACHE_TTL = 180  # seconds

    def __init__(self, initialze=False) -> None:
        """
        Args:
            initialize: Fetch stock data for available symbol immediately after init
        """
        self.symbols = settings.STOCKS.SYMBOLS.value
        self._cache = Cache(f"./stock_data.cache")
        if initialze:
            [self._fetch_stock_data(sym) for sym in self.symbols]

    def _get_from_cache(self, symbol: str):
        cached_data = self._cache.get(symbol, None)
        return cached_data

    def _find_closest_trading_date(self, df: pd.DataFrame, target_date: datetime) -> tuple[float, pd.Timestamp]:
        """
            Finds the Close-Price at the next trading day for the target date.
            Included weekends and holidays.
        """
        try:
            # Try to find the exact date
            return df.loc[target_date, 'Close'], target_date
        except KeyError:
            # Find next available date (search backward)
            available_dates = df.index[df.index <= target_date]
            if len(available_dates) == 0:
                # If no dates are available take the first
                return df.iloc[0]['Close'], df.index[0]

            # Last trading day before or on the taget date
            closest_date = available_dates[-1]
            return df.loc[closest_date, 'Close'], closest_date

    def _fetch_stock_data(self, symbol: str) -> StockData:
        """
        Calculates performance values for:
        - 1d
        - 7d
        - 14d
        - 1m
        - 6m
        """
        ticker = yf.Ticker(symbol)

        # Get history data for 1y for maximum precision
        hist = ticker.history(period="1y", interval="1d")

        if hist.empty:
            log.warning(f"No data for symbol {symbol} available")

        # today's date and latest price
        today = hist.index[-1]
        close_current = hist["Close"].iloc[-1]

        # === Calculate periods ===

        # day before
        date_1d = today - timedelta(days=1)
        close_1d, _ = self._find_closest_trading_date(hist, date_1d)

        # 7d ago
        date_7d = today - timedelta(days=7)
        close_7d, _ = self._find_closest_trading_date(hist, date_7d)

        # 14d ago
        date_14d = today - timedelta(days=14)
        close_14d, _ = self._find_closest_trading_date(hist, date_14d)

        # 1m ago (calender month!)
        date_1m = today - relativedelta(months=1)
        close_1m, _ = self._find_closest_trading_date(hist, date_1m)

        # 6m: Vor 6 Kalendermonaten
        date_6m = today - relativedelta(months=6)
        close_6m, _ = self._find_closest_trading_date(hist, date_6m)

        # === CALCULATE PERFORMANCE ===
        # Formula: ((current - historical) / historical) × 100
        def calc_performance(current: float, historical: float) -> tuple[float, float]:
            abs_change = current - historical
            pct_change = (abs_change / historical) * \
                100 if historical != 0 else 0.0
            return abs_change, pct_change

        change_1d_abs, change_1d_pct = calc_performance(
            close_current, close_1d)
        change_7d_abs, change_7d_pct = calc_performance(
            close_current, close_7d)
        change_14d_abs, change_14d_pct = calc_performance(
            close_current, close_14d)
        change_1m_abs, change_1m_pct = calc_performance(
            close_current, close_1m)
        change_6m_abs, change_6m_pct = calc_performance(
            close_current, close_6m)

        # === METADATA ===
        info = ticker.info
        name = info.get("longName", info.get("shortName", None))
        currency = info.get("currency", "")

        return StockData(
            symbol=symbol,
            name=name,
            currency=map_currency_to_symbol(currency),
            last_updated=datetime.now(),
            close_current=round(close_current, 2),
            change_1d_abs=round(change_1d_abs, 2),
            change_1d_pct=round(change_1d_pct, 2),
            change_7d_abs=round(change_7d_abs, 2),
            change_7d_pct=round(change_7d_pct, 2),
            change_14d_abs=round(change_14d_abs, 2),
            change_14d_pct=round(change_14d_pct, 2),
            change_1m_abs=round(change_1m_abs, 2),
            change_1m_pct=round(change_1m_pct, 2),
            change_6m_abs=round(change_6m_abs, 2),
            change_6m_pct=round(change_6m_pct, 2),
        )

    def get(self, symbol: str) -> StockData:
        cached = cast(StockData, self._get_from_cache(symbol))
        if cached is not None:
            return cached
        log.info(f"Cache miss for '{symbol}': Data acquisition started")

        new_data: StockData = self._fetch_stock_data(symbol)
        self._cache.set(symbol, new_data, expire=self.CACHE_TTL)

    def get_by_idx(self, idx: int) -> StockData:
        return self.get(self.symbols[idx])

from typing import Literal
from .crypto_market_data import CryptoMarketData
from src.utils import get_historical_perps, get_instruments_data

class PerpetualsData(CryptoMarketData):
    __type = 'perpetual'
    def __init__(self, currency: Literal["BTC", "ETH"], start: str, end: str, granularity: Literal['5m', '15m', '30m','1h', '2h', '4h', '6h', '12h', '1d']) -> None:
        super().__init__(currency, start, end, granularity)
        self.__instruments_data = get_instruments_data(currency, self.type())

    @classmethod
    def type(cls):
        return cls.__type
    
    @property
    def instruments_data(self):
        return self.__instruments_data
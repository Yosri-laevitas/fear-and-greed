from typing import Literal
import pandas as pd
from .crypto_market_data import CryptoMarketData
from src.utils import geq, get_historical_all_perps

class PerpetualsData():
    __type = 'perpetual'
    def __init__(self, currency: Literal["BTC", "ETH"], start: str, end: str, granularity: Literal['5m', '15m', '30m','1h', '2h', '4h', '6h', '12h', '1d']) -> None:
        self.__currency = currency
        self.__start = start
        self.__end = end
        self.__granularity = granularity
        self.__historical_data = get_historical_all_perps(self.__currency, self.__start, self.__end, self.__granularity)

    @classmethod
    def type(cls):
        return cls.__type
    
    @property
    def historical_data(self):
        return self.__historical_data
    
    @property
    def currency(self) -> Literal["BTC", "ETH"]:
        return self.__currency
    
    @currency.setter
    def currency(self, currency: Literal["BTC", "ETH"]) -> None:
        if self.__currency == currency:
            pass
        else:
            self.__currency = currency
            self.__historical_data = get_historical_all_perps(self.__currency, self.__start, self.__end, self.__granularity)

    @property
    def start(self) -> str:
        return self.__start
    
    @start.setter
    def start(self, start: str) -> None:
        if geq(start, self.__start):
            self.__historical_data = self.__historical_data[self.__historical_data['date']>=start]
        else:
            df = get_historical_all_perps(self.__currency, start, self.__start,self.__granularity)[:-1]
            self.__historical_data = pd.concat([df, self.__historical_data], axis=0, ignore_index=True)
        self.__start = start
    
    @property
    def end(self) -> str:
        return self.__end
    
    @end.setter
    def end(self, end: str) -> None:
        if geq(self.__end, end):
           self.__historical_data = self.__historical_data[self.__historical_data['date']<=end]
        else:
            df = get_historical_all_perps(self.__currency, self.__end, end, self.__granularity)[1:]
            self.__historical_data = pd.concat([self.__historical_data, df], axis=0, ignore_index=True)
        self.__end = end
    
    @property
    def granularity(self) -> str:
        return self.__granularity
    
    @granularity.setter
    def granularity(self, granularity: str) -> None:
        self.__granularity = granularity
        self.__historical_data = get_historical_all_perps(self.__currency, self.__start, self.__end, self.__granularity)
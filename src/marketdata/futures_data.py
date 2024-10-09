from typing import Literal
import pandas as pd
from .crypto_market_data import CryptoMarketData
from src.utils import geq, process_futures
from src.services import get_data


class FuturesData(CryptoMarketData):
    __type = "futures"

    def __init__(
        self,
        currency: Literal["BTC", "ETH"],
        start: str,
        end: str,
    ) -> None:
        self.__currency = currency
        self.__start = start
        self.__end = end

        self.__historical_data = process_futures(
            get_data(self.__currency, self.type(), self.__start, self.__end)
        )
        super().__init__()

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
            self.__historical_data = process_futures(
                get_data(self.__currency, self.type(), self.__start, self.__end)
            )

    @property
    def start(self) -> str:
        return self.__start

    @start.setter
    def start(self, start: str) -> None:
        if geq(start, self.__start):
            self.__historical_data = self.__historical_data[
                self.__historical_data["date"] >= start
            ]
        else:
            df = process_futures(
                get_data(self.__currency, self.type(), start, self.__start)
            )[:-1]
            self.__historical_data = pd.concat(
                [df, self.__historical_data], axis=0, ignore_index=True
            )
        self.__start = start

    @property
    def end(self) -> str:
        return self.__end

    @end.setter
    def end(self, end: str) -> None:
        if geq(self.__end, end):
            self.__historical_data = self.__historical_data[
                self.__historical_data["date"] <= end
            ]
        else:
            df = process_futures(
                get_data(self.__currency, self.type(), self.__end, end)
            )[1:]
            self.__historical_data = pd.concat(
                [self.__historical_data, df], axis=0, ignore_index=True
            )
        self.__end = end

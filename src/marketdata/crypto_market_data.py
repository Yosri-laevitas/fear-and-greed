from typing import Literal
# from src.utils import get_instruments_data


class CryptoMarketData:
    """
    A class to represent cryptocurrency market data.

    Attributes
    ----------
    currency : Literal["BTC", "ETH"]
        The cryptocurrency symbol.
    type : Literal['perpetual', 'option', 'future']
        The type of the instrument.
    start : str
        The start date for the data in 'YYYY-MM-DD' format.
    end : str
        The end date for the data in 'YYYY-MM-DD' format.
    granularity : Literal['5m', '15m', '30m','1h', '2h', '4h', '6h', '12h', '1d']
        The time interval for the data.

    Properties
    ----------
    currency
        Getter and setter for the currency.
    start
        Getter and setter for the start date.
    end
        Getter and setter for the end date.
    granularity
        Getter and setter for the granularity.
    """

    """fetcher_dict = {
        'perpetual':get_historical_all_perps,
        'option': get_historical_all_options,
        'future': get_historical_all_futures
    }"""

    def __init__(
        self,
        currency: Literal["BTC", "ETH"],
        type: Literal["perpetual", "option", "future"],
        start: str,
        end: str,
        granularity: Literal["5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d"],
    ) -> None:
        """
        Initializes a new instance of CryptoMarketData.

        Parameters
        ----------
        currency : Literal["BTC", "ETH"]
            The cryptocurrency symbol.
        type : Literal['perpetual', 'option', 'future']
            The type of the instrument.
        start : str
            The start date for the data in 'YYYY-MM-DD' format.
        end : str
            The end date for the data in 'YYYY-MM-DD' format.
        granularity : Literal['5m', '15m', '30m','1h', '2h', '4h', '6h', '12h', '1d']
            The time interval for the data.
        """
        self.__currency = currency
        self.__start = start
        self.__end = end
        self.__granularity = granularity
        self.__type = type

    @property
    def currency(self) -> Literal["BTC", "ETH"]:
        return self.__currency

    @currency.setter
    def currency(self, currency: Literal["BTC", "ETH"]) -> None:
        self.__currency = currency

    @property
    def start(self) -> str:
        return self.__start

    @start.setter
    def start(self, start: str) -> None:
        self.__start = start

    @property
    def end(self) -> str:
        return self.__end

    @end.setter
    def end(self, end: str) -> None:
        self.__end = end

    @property
    def granularity(self) -> str:
        return self.__granularity

    @granularity.setter
    def granularity(self, granularity: str) -> None:
        self.__granularity = granularity

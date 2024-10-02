import requests
import yaml
from typing import Literal
from pprint import pprint
def get_historical_perps(market: str, symbol: str, token: str, start: str, end: str, granularity: Literal['5m', '15m', '30m', '1h', '2h', '4h', '6h', '12h', '1d'], limit: int = 144, page: int = 1) -> dict:
    """
    Fetches historical data for perpetual swaps from the Laevitas API.

    Parameters
    ----------
    market : str
        The market for which the data is required.
    symbol : str 
        The symbol of the asset for which the data is required.
    token : str 
        The API token for authentication.
    start : str 
        The start date for the data in 'YYYY-MM-DD' format.
    end : str 
        The end date for the data in 'YYYY-MM-DD' format.
    granularity : str 
        The time interval for the data. Options: 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d.
    limit : int, optional 
        The maximum number of data points per page to retrieve. Default is 144.
    page : int, optional 
        The page number for pagination. Default is 1.

    Returns
    -------
    dict 
        A json containing the historical data for the specified perpetual swap.
    """

    params = {
        'start': start,
        'end': end,
        'granularity': granularity,
        'limit': limit,
        'page': page
    }

    headers = {
        'apiKey': token,
    }

    url = f'https://api.laevitas.ch/historical/derivs/perpetuals/{market}/{symbol}'

    response = requests.get(url=url, params=params, headers=headers)

    return response.json()


if __name__ == "__main__":

    with open('config/secrets.yml', 'r') as file:
        secrets = yaml.safe_load(file)

    market = 'DERIBIT'
    symbol = 'BTC-PERPETUAL'
    token = secrets.get('api', {}).get('crypto_data', {}).get('key')
    start = '2023-09-30'
    end = '2023-10-30'
    granularity = '1d'

    historical_data = get_historical_perps(market, symbol, token, start, end, granularity)
    pprint(historical_data)
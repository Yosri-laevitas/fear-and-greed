import requests
import yaml
from typing import Literal
from numpy import ceil
from pprint import pprint

import pandas as pd
def get_historical_perps_page(market: str, symbol: str, token: str, start: str, end: str, granularity: Literal['5m', '15m', '30m', '1h', '2h', '4h', '6h', '12h', '1d'], limit: int = 144, page: int = 1) -> dict:
    """
    Fetches historical data for perpetual swaps from the Laevitas API per page.

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
        A json containing a page of the historical data for the specified perpetual swap.
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

def get_df_items(items: list) -> pd.DataFrame:
    """
    Parses the 'items' field of the JSON data into a pandas DataFrame.

    Parameters
    ----------
    json_data : dict
        The JSON data containing the historical data.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the 'items' field of the JSON data.
    """ 
    df = pd.DataFrame(items)
    df['date'] = pd.to_datetime(df['date'], unit='ms')
    return df

def get_historical_perps(market: str, symbol: str, token: str, start: str, end: str, granularity: Literal['5m', '15m', '30m', '1h', '2h', '4h', '6h', '12h', '1d'], limit: int = 144):
    
    historical_data = get_historical_perps_page(market, symbol, token, start, end, granularity, limit)
    
    items = historical_data['items']

    total_items = historical_data['meta']['total']
    items_per_page = historical_data['meta']['items']
    pages = int(ceil(total_items / items_per_page))

    for page in range(2, pages + 1):
        historical_data = get_historical_perps_page(market, symbol, token, start, end, granularity, limit, page)
        items += historical_data['items']
    
    return items

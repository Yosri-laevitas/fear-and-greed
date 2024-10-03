import requests
from typing import Literal
import yaml
import pandas as pd
import numpy as np

base_url = 'https://api.laevitas.ch'

with open('config/secrets.yml', 'r') as file:
    secrets = yaml.safe_load(file)

token = secrets.get('api', {}).get('crypto_data', {}).get('key')

headers = {
        'apiKey': token,
    }

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
    pd.set_option("future.no_silent_downcasting", True)
    df = df.replace({None: np.nan})

    return df

# ----------------------------------------------------------------
# Instruments Data Fetchers
# ----------------------------------------------------------------

def get_instruments_data() -> pd.DataFrame:
    """
    Fetches instrument data from the Laevitas API.

    Returns
    -------
    dict
        The JSON response containing the instrument data.
    """
    url = base_url + '/analytics/futures/instruments'
    response = requests.get(url=url, headers=headers)
    return pd.DataFrame(response.json()['data'])

# ----------------------------------------------------------------
# Perps Data Fetchers
# ----------------------------------------------------------------

def get_historical_perps_page(market: str, 
                              symbol: str, 
                              start: str, 
                              end: str, 
                              granularity: Literal['5m', '15m', '30m', '1h', '2h', '4h', '6h', '12h', '1d'], 
                              limit: int = 144, 
                              page: int = 1
                             ) -> dict:
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

    url = base_url + f'/historical/derivs/perpetuals/{market}/{symbol}'

    response = requests.get(url=url, params=params, headers=headers)

    return response.json()

def get_historical_perps(market: str, 
                         symbol: str, 
                         start: str,
                         end: str, 
                         granularity: Literal['5m', '15m', '30m','1h', '2h', '4h', '6h', '12h', '1d'], 
                         limit: int = 144
                        ) -> list:
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
    
    Returns
    -------
    list
        A list containing all the historical data points for the specified perpetual swap.
    """

    historical_data = get_historical_perps_page(market, symbol, start, end, granularity, limit)
    items = historical_data['items']
    pages = historical_data['meta']['total_pages']

    for page in range(2, pages + 1):
        historical_data = get_historical_perps_page(market, symbol, start, end, granularity, limit, page)
        items += historical_data['items']
    
    return items

# ----------------------------------------------------------------
# Futures Data Fetchers
# ----------------------------------------------------------------

def get_historical_futures_page(market: str, symbol: str, start: str, end: str, granularity: Literal['1m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '12h', '1d'], limit: int = 144, page: int = 1) -> dict:
    """
    Fetches historical data for futures contracts from the Laevitas API per page.

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
        The time interval for the data. Options: 1m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 12h, 1d.
    limit : int, optional
        The maximum number of data points per page to retrieve. Default is 144.
    page : int, optional
        The page number for pagination. Default is 1.
    
    Returns
    -------
    dict
        A json containing a page of the historical data for the specified futures contract.
    """
    
    params = {
        'start': start,
        'end': end,
        'granularity': granularity,
        'limit': limit,
        'page': page
    }
    
    url = f'https://api.laevitas.ch/historical/derivs/futures/{market}/{symbol}'
    
    response = requests.get(url=url, params=params, headers=headers)
    
    return response.json()


# ----------------------------------------------------------------
# Options Data Fetchers
# ----------------------------------------------------------------


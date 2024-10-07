from time import sleep
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
    df = df.replace({None: np.nan})

    return df

# ----------------------------------------------------------------
# Instruments Data Fetchers
# ----------------------------------------------------------------

def get_instruments_data(currency: Literal['BTC', 'ETH'] = None, type: Literal['perpetual', 'option', 'future'] = None) -> pd.DataFrame:
    """
    Fetches instrument data from the Laevitas API.

    Parameters
    ----------
    currency : Literal['BTC', 'ETH']
        The currency of the instruments to retrieve. Default is None.
    type : Literal['perpetual', 'option', 'future']
        The type of instruments to retrieve. Default is None.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the 'market' and 'instrument' columns of the filtered instrument data.
    """
    
    url = f"{base_url}/analytics/futures/instruments"
    target_cols  = ['market', 'instrument'] 
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json().get('data', [])
        
        if not data:
            raise ValueError("No data returned from API.")
        
        df = pd.DataFrame(data)
        filtered_df = df.copy()
        
        if currency is not None: 
            filtered_df = filtered_df[filtered_df['currency'] == currency]
        if type is not None:
            filtered_df = filtered_df[filtered_df['type'] == type]

        if currency is None:
            target_cols += ['currency']
        if type is None:
            target_cols += ['type']
        
        return filtered_df[target_cols].drop_duplicates().reset_index(drop=True)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return pd.DataFrame()
    except ValueError as ve:
        print(ve)
        return pd.DataFrame()

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
    Fetches historical data for a specified perpetual from the Laevitas API per page.

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
        A json containing a page of the historical data for the specified perpetual.
    """
    sleep(2)

    params = {
        'start': start,
        'end': end,
        'granularity': granularity,
        'limit': limit,
        'page': page,
        'legacy':'true'
    }

    url = base_url + f'/historical/derivs/perpetuals/{market}/{symbol}'

    response = requests.get(url=url, params=params, headers=headers)

    if response.status_code != 200:
        print(f'Error ({market}, {symbol}): {response.text}')
        sleep(5)
        response = requests.get(url=url, params=params, headers=headers)
        if response.status_code!= 200:
            print(f'Error second try ({market}, {symbol}): {response.text}')
            return

    return response.json()

def get_historical_perps(market: str, 
                         symbol: str, 
                         start: str,
                         end: str, 
                         granularity: Literal['5m', '15m', '30m','1h', '2h', '4h', '6h', '12h', '1d'], 
                         limit: int = 144
                        ) -> pd.DataFrame:
    """
    Fetches historical data for a specified perpetual from the Laevitas API.

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
    pd.DataFrame
        A dataframe containing all the historical data points for the specified perpetual.
    """

    historical_data = get_historical_perps_page(market, symbol, start, end, granularity, limit)
    if historical_data:
        items = historical_data['items']
        total_items = historical_data['meta']['total']
        pages = int(np.ceil(total_items / limit))

        for page in range(2, pages + 1):
            historical_data = get_historical_perps_page(market, symbol, start, end, granularity, limit, page)
            items += historical_data['items']
        
        if items:
            return get_df_items(items)
    print('No items to return00')
    return None

# ----------------------------------------------------------------
# Futures Data Fetchers
# ----------------------------------------------------------------

def get_historical_futures_page(market: str, symbol: str, start: str, end: str, granularity: Literal['1m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '12h', '1d'], limit: int = 144, page: int = 1) -> dict:
    """
    Fetches historical data for a specified futures contract from the Laevitas API per page.

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
    sleep(2)

    params = {
        'start': start,
        'end': end,
        'granularity': granularity,
        'limit': limit,
        'page': page
    }
    
    url = base_url + f'/historical/derivs/futures/{market}/{symbol}'
    
    response = requests.get(url=url, params=params, headers=headers)
    
    return response.json()

def get_historical_futures(market: str, 
                           symbol: str, 
                           start: str,
                           end: str, 
                           granularity: Literal['5m', '15m', '30m','1h', '2h', '4h', '6h', '12h', '1d'], 
                           limit: int = 144
                          ) -> pd.DataFrame:
    """
    Fetches historical data for a specified futures contract from the Laevitas API.

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
    pd.DataFrame
        A dataframe containing all the historical data points for the specified futures.
    """

    historical_data = get_historical_futures_page(market, symbol, start, end, granularity, limit)
    items = historical_data['items']
    pages = historical_data['meta']['total_pages']

    for page in range(2, pages + 1):
        historical_data = get_historical_futures_page(market, symbol, start, end, granularity, limit, page)
        items += historical_data['items']
    
    return get_df_items(items)

# ----------------------------------------------------------------
# Options Data Fetchers
# ----------------------------------------------------------------

def get_historical_options_page(market: str, 
                                instrument: str, 
                                start: str, 
                                end: str, 
                                granularity: Literal['5m', '15m', '30m','1h', '2h', '4h', '6h', '12h', '1d'], 
                                limit: int = 144, 
                                page: int = 1
                               ) -> dict:
    """
    Fetches historical data for a specified options contract from the Laevitas API per page.

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
        A json containing a page of the historical data for the specified options contract.
    """
    sleep(2)

    params = {
        'start': start,
        'end': end,
        'granularity': granularity,
        'limit': limit,
        'page': page
    }
    
    url = f'{base_url}/historical/options/{market}/{instrument}'
    
    response = requests.get(url=url, params=params, headers=headers)
    
    return response.json()

def get_historical_options(market: str, 
                           instrument: str, 
                           start: str, 
                           end: str,
                           granularity: Literal['5m', '15m', '30m','1h', '2h', '4h', '6h', '12h', '1d'], 
                           limit: int = 144
                           ) -> pd.DataFrame:
    """
    Fetches historical data for options from the Laevitas API.

    Parameters
    ----------
    market : str
        The market for which the data is required.
    instrument : str 
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
    pd.DataFrame
        A dataframe containing all the historical data points for the specified options.
    """
    
    historical_data = get_historical_options_page(market, instrument, start, end, granularity, limit)
    items = historical_data['items']
    total_items = historical_data['meta']['total']
    pages = int(np.ceil(total_items / limit))
    
    for page in range(2, pages + 1):
        historical_data = get_historical_options_page(market, instrument, start, end, granularity, limit, page)
        items += historical_data['items']
    
    return get_df_items(items)
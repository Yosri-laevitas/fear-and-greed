from time import sleep
import requests
from typing import Literal
import yaml
import pandas as pd
import numpy as np
import logging
from logging.handlers import RotatingFileHandler
import warnings

handler = RotatingFileHandler(
    'logs/data_fetchers.log', maxBytes=5*1024*1024, backupCount=3  # 5MB file size with 3 backups
)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[handler]
)

perps_logger = logging.getLogger('perps_logger')
futures_logger = logging.getLogger('futures_logger')
options_logger = logging.getLogger('options_logger')
instruments_logger = logging.getLogger('instruments_logger')

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

def get_instruments_data(currency: Literal['BTC', 'ETH'] = None, 
                         type: Literal['perpetual', 'option', 'future'] = None) -> pd.DataFrame:
    """
    Fetches instrument data from the Laevitas API.

    Parameters
    ----------
    currency : Literal['BTC', 'ETH'], optional
        The currency of the instruments to retrieve. Default is None.
    type : Literal['perpetual', 'option', 'future'], optional
        The type of instruments to retrieve. Default is None.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the 'market' and 'instrument' columns of the filtered instrument data.
    """
    
    url = f"{base_url}/analytics/futures/instruments"
    target_cols = ['market', 'instrument'] 
    instruments_logger.info("Fetching instrument data from API")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json().get('data', [])
        
        if not data:
            instruments_logger.warning("No data returned from API")
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

        instruments_logger.info(f"Successfully retrieved and filtered instrument data (Currency: {currency}, Type: {type})")
        return filtered_df[target_cols].drop_duplicates().reset_index(drop=True)

    except requests.exceptions.RequestException as e:
        instruments_logger.error(f"API request error: {e}")
        return pd.DataFrame()
    
    except ValueError as ve:
        instruments_logger.error(f"Data validation error: {ve}")
        return pd.DataFrame()

# ----------------------------------------------------------------
# Perps Data Fetchers
# ----------------------------------------------------------------

def get_historical_perps_page(market: str, 
                              symbol: str, 
                              start: str, 
                              end: str, 
                              granularity: str, 
                              limit: int = 144, 
                              page: int = 1) -> dict:
    """
    Fetches historical data for a specified perpetual from the Laevitas API per page.

    Parameters
    ----------
    market : str
        The market for which the data is required.
    symbol : str 
        The symbol of the asset for which the data is required.
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
    perps_logger.info(f"Requesting historical perps data (Market: {market}, Symbol: {symbol}, Page: {page})")
    
    sleep(1)
    url = f'{base_url}/historical/derivs/perpetuals/{market}/{symbol}'
    params = {
        'start': start,
        'end': end,
        'granularity': granularity,
        'limit': limit,
        'page': page,
        'legacy': 'true'
    }

    try:
        response = requests.get(url=url, params=params, headers=headers)
        response.raise_for_status()
        perps_logger.info(f"Successfully retrieved page {page} of historical perps data for {symbol}")
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        perps_logger.error(f"HTTP error occurred: {http_err} | Retrying... (Market: {market}, Symbol: {symbol}, Page: {page})")
        sleep(2)  # Wait before retrying
        try:
            response = requests.get(url=url, params=params, headers=headers)
            response.raise_for_status()
            perps_logger.info(f"Successfully retrieved data after retry (Market: {market}, Symbol: {symbol}, Page: {page})")
            return response.json()
        except requests.exceptions.RequestException as err:
            perps_logger.error(f"Failed on retry for {symbol} | Error: {err}")
            return None
    except Exception as e:
        perps_logger.error(f"Unexpected error: {e}")
        return None


def get_historical_perps(market: str, 
                         symbol: str, 
                         start: str, 
                         end: str, 
                         granularity: str, 
                         limit: int = 144) -> pd.DataFrame:
    """
    Fetches historical data for a specified perpetual from the Laevitas API.

    Parameters
    ----------
    market : str
        The market for which the data is required.
    symbol : str 
        The symbol of the asset for which the data is required.
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
    if market =='OKEX':
        market = 'OKX'
    perps_logger.info(f"Fetching full historical perps data for {market}'s {symbol}")

    historical_data = get_historical_perps_page(market, symbol, start, end, granularity, limit)
    
    if historical_data and 'items' in historical_data:
        items = historical_data['items']
        total_items = historical_data['meta']['total']
        pages = int(np.ceil(total_items / limit))

        perps_logger.info(f"Total items: {total_items}, Pages to retrieve: {pages}")

        for page in range(2, pages + 1):
            perps_logger.info(f"Fetching page {page} for {symbol}")
            more_data = get_historical_perps_page(market, symbol, start, end, granularity, limit, page)
            if more_data and 'items' in more_data:
                items += more_data['items']

        if items:
            perps_logger.info(f"Successfully retrieved full historical data for {market}'s {symbol}")
            return get_df_items(items)

    perps_logger.error(f"No data returned for {market}'s {symbol}")
    return pd.DataFrame()

def get_historical_all_perps(currency: Literal['BTC', 'ETH'], 
                             start: str, 
                             end: str, 
                             granularity: str, 
                             limit: int = 144) -> pd.DataFrame:
    """
    Fetches historical data for all perpetuals for a specified currency.

    Parameters
    ----------
    currency : Literal['BTC', 'ETH']
        The currency for which to fetch historical perpetual data (BTC or ETH).
    start : str
        The start date for the data in 'YYYY-MM-DD' format.
    end : str
        The end date for the data in 'YYYY-MM-DD' format.
    granularity : str
        The time interval for the data. Options include: '5m', '15m', '30m', '1h', '2h', '4h', '6h', '12h', '1d'.
    limit : int, optional
        The maximum number of data points to retrieve per page (default is 144).

    Returns
    -------
    pd.DataFrame
        A DataFrame containing historical perpetual data for the specified currency across all markets.
    """
    perps_logger.info("*********************************************************************************************")
    perps_logger.info(f"Fetching historical data for all available perpetuals of {currency} from {start} to {end}")

    try:
        instrument_df = get_instruments_data(currency, 'perpetual')
        L_dfs = []
        perps_logger.info(f"Found {len(instrument_df)} perpetuals for {currency}")

        for row in instrument_df.itertuples():
            market = row.market
            symbol = row.instrument
            pd.set_option("future.no_silent_downcasting", True)
            
            df = get_historical_perps(market, symbol, start, end, granularity, limit)
            if df is not None and not df.empty:
                df['market'] = market
                df['symbol'] = symbol
                L_dfs.append(df)

        if L_dfs:
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                combined_df = pd.concat(L_dfs, axis=0, ignore_index=True)

                for warning in w:
                    if issubclass(warning.category, FutureWarning):
                        perps_logger.warning(f"FutureWarning: {warning.message}")
                    else:
                        perps_logger.warning(f"Warning: {warning.message}")
                        
            combined_df = pd.concat(L_dfs, axis=0, ignore_index=True)
            perps_logger.info("Successfully concatenated all fetched data")
            return combined_df[['date', 'market', 'symbol', 'price', 'basis', 'funding', 'volume', 'open_interest', 'long_short_ratio']].drop_duplicates(subset=['date', 'market', 'symbol'])
        else:
            perps_logger.warning(f"No data found for any perpetual in {currency}")
            return pd.DataFrame()

    except Exception as e:
        perps_logger.error(f"An error occurred while fetching historical perps data: {e}")
        return pd.DataFrame()


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
import requests
import yaml
from pprint import pprint
def get_historical_perps(market: str, symbol: str, token: str, start: str, end: str, granularity: str, limit: int = 144, page: int = None):

    params = {
        'start': start,
        'end': end,
        'granularity': granularity,
        'limit': limit,
        'page':page
    }

    headers = {
        'apiKey':token,
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

    historical_data = get_historical_perps(market, symbol, token, start, end, granularity, page=1)
    pprint(historical_data)
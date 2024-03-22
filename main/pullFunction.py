from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd

def api_runner():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
    'start':'1',
    'limit':'10',
    'convert':'USD'
    }
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': 'bc2d9296-8aa2-4f85-8f7d-c1fb641707c4',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        df = pd.json_normalize(data['data'])
        df['timestamp'] = pd.to_datetime('now')
        return df

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
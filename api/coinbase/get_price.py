import requests
from ..api_configure import config
def get_price(coin_id: str) -> dict:
    url = config.coinbase.url.format(coin_id=coin_id)
    response = requests.get(url)
    if response.status_code == 200:
        data_out = response.json()
        return data_out['data']['amount']
    else:
        print("Error Coinbase:", response.status_code, response.text)
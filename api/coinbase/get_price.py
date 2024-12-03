import requests
from ..api_configure import config

def get_price(coin_id: str) -> float:
    url = config.coinbase.url.format(coin_id=coin_id)
    # print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data_out = response.json()
        price = data_out['data']['amount']
        # print(price)
        return price
    else:
         print("Error Coinbase:", response.status_code, response.text)
         return 0
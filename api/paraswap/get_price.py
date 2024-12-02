import requests
from ..api_configure import config
from .apiModel import ParaswapApi
import json

def get_price(coin_id: str) -> int:
    # print(coin_id)
    data = ParaswapApi().get_price(['0xdac17f958d2ee523a2206206994597c13d831ec7', coin_id])
    # print(json.dumps(data, indent=4))
    decimal = int(data['priceRoute']['srcDecimals'])

    price = int(data['priceRoute']['bestRoute'][0]['swaps'][0]['swapExchanges'][0]['srcAmount'])
    # print(price)
    return 1/ (price / (10**decimal) / 1000)

# print(get_price('0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'))
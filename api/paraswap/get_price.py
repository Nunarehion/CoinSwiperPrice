import requests
from ..api_configure import config
from .apiModel import ParaswapApi
# import json

def get_price(coin_id: str) -> float:
    # print(coin_id)
    # print(json.dumps(data, indent=4))
    data = ParaswapApi().get_price(['0xdac17f958d2ee523a2206206994597c13d831ec7', coin_id])
    decimal = int(data['priceRoute']['srcDecimals'])
    price = int(data['priceRoute']['bestRoute'][0]['swaps'][0]['swapExchanges'][0]['srcAmount'])
    gas_fee = float(data['priceRoute']['gasCostUSD'])
    return {
        "price": 1 / (price / (10 ** decimal) / 1000),
        "gas_fee": gas_fee
    }


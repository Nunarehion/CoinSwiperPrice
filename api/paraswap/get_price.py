import requests
from ..api_configure import config
from .apiModel import ParaswapApi
    

def get_price(coin_id: str) -> int:
    return ParaswapApi().get_price('0xdac17f958d2ee523a2206206994597c13d831ec7', coin_id)['priceRoute']['bestRoute'][0]['swaps'][0]['swapExchanges'][0]['srcAmount']


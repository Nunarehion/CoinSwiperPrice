from . import *
import data.coins
#from models.coin import Coin
import time
from dataclasses import dataclass
from typing import List

def get_all_price():
    result = {"uniswap": [], "coinbase": [], "coin": []}
    for coin in data.coins.coins_data:
        try:
            result["coinbase"].append(coinbase.get_price(coin['symbol']))
            result["uniswap"].append(uniswap.get_price(coin['token']))
            result["coin"].append(coin)
            time.sleep(1)
        except:
            print('Error', coin)
    return result

@dataclass
class Exchange:
    name: str
    price: int

@dataclass
class CryptoData:
    token: str
    symbol: str
    exchanges: List[Exchange]
    difference: float
    percent: float

all_result = []

prices = get_all_price()
for i in range(len(prices["coin"])):
    coin = prices["coin"][i]
    uniswap_price = float(prices["uniswap"][i])
    coinbase_price = float(prices["coinbase"][i])
    dif = uniswap_price - coinbase_price
    if dif != 0:
        percentage_difference = (dif / coinbase_price) * 100
    else:
        percentage_difference = 0
    data = CryptoData(
    token = coin['symbol'],
    symbol = coin['name'],
    exchanges=[
        Exchange(name="coinbase", price=coinbase_price),
        Exchange(name="uniswap", price=uniswap_price)
    ],
    difference = dif,
    percent = percentage_difference
    )
    all_result.append(data)

def print_crypto_data(all_result):
    for crypto_data in all_result:
        print(f"Token: {crypto_data.token}")
        print(f"Symbol: {crypto_data.symbol}")
        print("Exchanges:")
        for exchange in crypto_data.exchanges:
            print(f"  - {exchange.name}: {exchange.price}")
        print(f"Price Difference: {crypto_data.difference}")
        print(f"Percentage Difference: {crypto_data.percent:.2f}%")
        print()
from . import *
import data.coins
#from models.coin import Coin
import time
from dataclasses import dataclass
from typing import List
from models.coin import Exchange
from models.coin import CryptoData

def get_all_price():
    all_data = []
    for coin in data.coins.coins_data:
        print(coin)
        try:
            coinbase_price = float(coinbase.get_price(coin['symbol']))
            uniswap_price = float(paraswap.get_price(coin['address']))
            dif = uniswap_price - coinbase_price
            if dif != 0:
                percentage_difference = (dif / coinbase_price) * 100
            else:
                percentage_difference = 0
            crypto_data  = CryptoData(
            token = coin['symbol'],
            symbol = coin['token'],
            exchanges=sorted([
                Exchange(name="coinbase", price=coinbase_price),
                Exchange(name="uniswap", price=uniswap_price)
            ],key =lambda obj: obj.price),
            difference = abs(dif),
            percent = abs(round(percentage_difference, 5))
            )
            all_data.append(crypto_data)
            time.sleep(1)
        except Exception as e:
            print("ERROR (FUNC GET_ALL_PRICE)::",e)
    return all_data
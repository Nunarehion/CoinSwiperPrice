from . import *
import data.coins
#from models.coin import Coin
import time
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
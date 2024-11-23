import api
import data.coins
import time
from api.api_client import get_all_price
# coin = data.coins.coins_data[0]
# print(api.coinbase.get_price(coin['symbol']))
# print(api.uniswap.get_price(coin['token']))

print(get_all_price())
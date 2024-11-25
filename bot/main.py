import api
import data.coins
import time
from api.api_client import get_all_price
from api.api_client import all_result
from api.api_client import print_crypto_data

# coin = data.coins.coins_data[0]
# print(api.coinbase.get_price(coin['symbol']))
# print(api.uniswap.get_price(coin['token']))

#print(get_all_price())
print(print_crypto_data(all_result))
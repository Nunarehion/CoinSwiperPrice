from . import *  # noqa: F403
import data.coins
#from models.coin import Coin
import time
from dataclasses import dataclass
from typing import List
from models.coin import Exchange
from models.coin import CryptoData
from .paraswap.get_price import get_price

def get_all_price() -> List[CryptoData]:
    """
    Получает цены всех криптовалют с различных бирж.

    Эта функция проходит по всем доступным криптовалютам из data.coins, получает их цены с 
    биржи (Coinbase и Paraswap), вычисляет разницу между этими ценами и 
    процентное отклонение. Затем она создает объекты CryptoData для каждой 
    криптовалюты и добавляет их в список.

    Returns:
        List[CryptoData]: Список объектов CryptoData, содержащих информацию о ценах 
        для каждой криптовалюты, включая название токена, адрес, цены с бирж и 
        разницу в ценах.
    """
    all_data = []
    for coin in data.coins.coins_data:
        try:
            coinbase_price = float(coinbase.get_price(coin['symbol']))
            paraswap_price1 = paraswap.get_price(coin['address'])
            paraswap_price= float(paraswap_price1['price'])
            gas_fee = float(paraswap_price1['gas_fee'])
            dif = paraswap_price - coinbase_price
            if dif != 0:
                percentage_difference = (dif / coinbase_price) * 100
            else:
                percentage_difference = 0
            crypto_data  = CryptoData(
                        token      = coin['symbol'],
                        symbol     = coin['address'],
                        exchanges  = sorted([
                                        Exchange(name="coinbase", price= f"{round(coinbase_price, 5):.5f}"),
                                        Exchange(name="paraswap", price= f"{round(paraswap_price, 5):.5f}"),
                                        Exchange(name="paraswap_gas_fee", price=f"{round(gas_fee, 5):.5f}")
                                        ], key =lambda obj: obj.price ),
                        difference = abs(round(dif, 5)),
                        percent    = abs(round(percentage_difference, 5))
            )
            all_data.append(crypto_data)
            time.sleep(0.1)
        except Exception as e:
            print("ERROR (FUNC GET_ALL_PRICE)::", e)
    return all_data
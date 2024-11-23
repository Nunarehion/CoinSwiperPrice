import requests
import json
from adict import adict as OldAdict
import os
import time

def adict(data):
    if isinstance(data, dict):
        return OldAdict({k: adict(v) for k, v in data.items()})
    elif isinstance(data, list):
        return [adict(item) for item in data]
    else:
        return data



file_path = os.path.join('data', 'coins.json')
with open(file_path, 'r', encoding='utf-8') as file:
    coins_data = adict(json.load(file))




def get_price_uniswap(token: str) -> float:
    url = "https://interface.gateway.uniswap.org/v1/graphql"
    headers = {
        "accept": "*/*",
        "content-type": "application/json",
        "origin": "https://app.uniswap.org",
        "referer": "https://app.uniswap.org/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36",
    }

    payload = {
        "operationName": "TokenSpotPrice",
        "variables": {
            "address": f'{token}',
            "chain": "ETHEREUM"
        },
        "query": "query TokenSpotPrice($chain: Chain!, $address: String = null) {\n  token(chain: $chain, address: $address) {\n    id\n    address\n    chain\n    name\n    symbol\n    project {\n      id\n      markets(currencies: [USD]) {\n        id\n        price {\n          id\n          value\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        # print("Response JSON:", response.json())
        # print("Response JSON:", data.token.project.markets[0].price.value)
        if not data.token:
            print("err::", data)
        return float(data.token.project.markets[0].price.value)
    else:
        print("Error:", response.status_code, response.text)

def get_price_coinbase(coin_id: str) -> dict:
    #print(coin_id)
    url = f"https://api.coinbase.com/v2/prices/{coin_id}-USD/spot?currency=USD"
    response = requests.get(url)

    if response.status_code == 200:
        data_out = response.json()
        return adict(data_out)
    else:
        print("Ошибка при получении данных.")
        return None
#data_coinbase = get_price_coinbase('DAI').data.amount
#print(data_coinbase)
def get_all_price_uniswap() -> dict:
    prices = []
    for id in coins_data:
        try:
            coin = coins_data[id]
            token = coin.token
            price__uniswap = 0 #get_price_uniswap(token)
            price__coinbase = get_price_coinbase(id.upper()).data.amount
            time.sleep(0.5)
            item = {coin.name: OldAdict({"uniswap": price__uniswap, "coinbase": price__coinbase })} #get_price_coinbase(id.upper())}).data['data']['amount']
            prices.append(item)
            print(item)
        except Exception as e:
            print(e, coin.name, coin)
    return prices


print(get_all_price_uniswap())
ssh-keygen -t ed25519 -C "krakenmause@gmail.com"
ssh-keygen -t rsa -b 4096 -C "krakenmause@gmail.com"
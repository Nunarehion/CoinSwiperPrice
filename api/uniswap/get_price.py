import requests
import json
from ..api_configure import config
def get_price(token_address):
    url = config.uniswap.url

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
            "address": f'{token_address}',
            "chain": "ETHEREUM"
        },
        "query": "query TokenSpotPrice($chain: Chain!, $address: String = null) {\n  token(chain: $chain, address: $address) {\n    id\n    address\n    chain\n    name\n    symbol\n    project {\n      id\n      markets(currencies: [USD]) {\n        id\n        price {\n          id\n          value\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        data =  response.json()["data"]
        return data["token"]["project"]["markets"][0]["price"]["value"]
    else:
        print("Error Uniswap:", response.status_code, response.text)
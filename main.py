import requests
import json
from adict import adict as OldAdict

def adict(data):
    if isinstance(data, dict):
        return OldAdict({k: adict(v) for k, v in data.items()})
    elif isinstance(data, list):
        return [adict(item) for item in data]
    else:
        return data


# URL для запроса
url = "https://interface.gateway.uniswap.org/v1/graphql"

# Заголовки запроса
headers = {
    "accept": "*/*",
    "content-type": "application/json",
    "origin": "https://app.uniswap.org",
    "referer": "https://app.uniswap.org/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 YaBrowser/24.10.0.0 Safari/537.36",
}

# Тело запроса
payload = {
    "operationName": "TokenSpotPrice",
    "variables": {
        "address": '0x6b175474e89094c44da98b954eedeac495271d0f',  # Здесь вы можете указать адрес токена, если он известен
        "chain": "ETHEREUM"
    },
    "query": "query TokenSpotPrice($chain: Chain!, $address: String = null) {\n  token(chain: $chain, address: $address) {\n    id\n    address\n    chain\n    name\n    symbol\n    project {\n      id\n      markets(currencies: [USD]) {\n        id\n        price {\n          id\n          value\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
}

# Выполнение POST-запроса
response = requests.post(url, headers=headers, data=json.dumps(payload))

# Проверка статуса ответа
if response.status_code == 200:
    # Вывод результата
    data = adict(response.json()).data
    print("Response JSON:", response.json())
    print("Response JSON:", data.token.project.markets[0].price.value)
else:
    print("Error:", response.status_code, response.text)

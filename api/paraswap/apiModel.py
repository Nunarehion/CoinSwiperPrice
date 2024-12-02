from ..api_configure import config
from typing import List, Dict, Any, Literal, Union
import requests
import json
from utils import adict

class ParaswapApi:
    def __init__(self):
        self.url = config.paraswap.url
        self.endpoints = {
            "pairs": self.url + "/pairs",
            "swap": self.url + "/swap",
            "prices": self.url + "/prices",
            "tokens": self.url + '/tokens'
        }
        
    def get_tokens(self, network: Union[int, str] = 1):
        url = self.endpoints['tokens']
        response = requests.get(f"{url}/{str(network)}")
        if response.status_code == 200:
            data = response.json()['tokens']
            return data
            return json.dumps(data, indent=4)
        else:
            return f'Ошибка: {response.status_code}'
        
    def get_price(self,
                  tokens: List[str] = None, 
                  amount: int = 1000, 
                  side: Literal["BUY", "SELL"] = "BUY", 
                  network: Union[int, str] = '1', 
                  slippage: Union[int, str] = '1') -> Dict[str, Any]:
        params = {
            'destToken': tokens[0],
            'srcToken': tokens[1],
            'amount': str(amount * 10**6),
            'network': str(network),
            'slippage': str(slippage),
            'side': side,
        }
        url = self.endpoints['prices']
        response = requests.get(url, params)
        if response.status_code == 200:
            return adict(response.json())
        else:
            raise Exception(f"Ошибка {response.status_code}: {response.text}")

# print(ParaswapApi().get_price(
#     ['0xdac17f958d2ee523a2206206994597c13d831ec7', 
#         '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee'],
#     1
# ))

# with open('data.json', 'w') as json_file:
#     json.dump(ParaswapApi().get_tokens(), json_file, indent=4)
#print(ParaswapApi().get_tokens())

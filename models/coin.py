from dataclasses import dataclass
from typing import List
@dataclass
class Coin:
    token: str
    symbol: str
    exchange: str
    price: float

@dataclass
class Exchange:
    name: str
    price: str
    gas_fee: str

@dataclass
class CryptoData:
    token: str
    symbol: str
    exchanges: List[Exchange]
    difference: float
    percent: float
# Example usage
#crypto = Cryptocurrency(token="Bitcoin", symbol="BTC", exchange="Binance", price=45000.0)


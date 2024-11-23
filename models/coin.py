from dataclasses import dataclass

@dataclass
class Coin:
    token: str
    symbol: str
    exchange: str
    price: float

# Example usage
#crypto = Cryptocurrency(token="Bitcoin", symbol="BTC", exchange="Binance", price=45000.0)


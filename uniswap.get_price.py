from moralis import evm_api
from ..api_client import config

def get_price(token_address):
    #api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6ImVmZjA2MWJmLWNhZTItNGJjOC1iZTcyLTVhMWY3ZmU0YmY5YiIsIm9yZ0lkIjoiNDE2NjM2IiwidXNlcklkIjoiNDI4MjU4IiwidHlwZUlkIjoiZWYwYmEzZWUtMGJkMi00ODViLTg1YmMtOGQxNzEwMmU1ZWE0IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3MzE5MzgwMjEsImV4cCI6NDg4NzY5ODAyMX0.qM94E4-3WnE77zy2_EKy1TfvB7R9JpoIbitxhScUh-o"
    api_key = config.uniswap.api_key
    params = {
        "chain": "eth",
        "include": "percent_change",
        "exchange": "uniswapv2",
        "address": token_address
    }

    result = evm_api.token.get_token_price(
        api_key=api_key,
        params=params,
    )

    return result['usdPrice']
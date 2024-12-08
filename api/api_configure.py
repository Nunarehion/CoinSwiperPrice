import utils
config = utils.adict({
    "coinbase": {
        "url": "https://api.coinbase.com/v2/prices/{coin_id}-USD/spot?currency=USD"
    },
    "uniswap": {
        "api_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub25jZSI6ImVmZjA2MWJmLWNhZTItNGJjOC1iZTcyLTVhMWY3ZmU0YmY5YiIsIm9yZ0lkIjoiNDE2NjM2IiwidXNlcklkIjoiNDI4MjU4IiwidHlwZUlkIjoiZWYwYmEzZWUtMGJkMi00ODViLTg1YmMtOGQxNzEwMmU1ZWE0IiwidHlwZSI6IlBST0pFQ1QiLCJpYXQiOjE3MzE5MzgwMjEsImV4cCI6NDg4NzY5ODAyMX0.qM94E4-3WnE77zy2_EKy1TfvB7R9JpoIbitxhScUh-o",
        "url": "https://interface.gateway.uniswap.org/v1/graphql"
    },
    "paraswap": {
        "url": "https://api.paraswap.io"
    },
})
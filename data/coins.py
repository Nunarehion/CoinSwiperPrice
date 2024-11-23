import json
import os

file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'cryptocurrencies.json')

with open(file_path, 'r', encoding='utf-8') as file:
    coins_data = json.load(file)
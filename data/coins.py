import os
import json
file_path = os.path.join('data', 'coins.json')
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
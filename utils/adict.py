
from adict import adict as OldAdict
def adict(data):
    if isinstance(data, dict):
        return OldAdict({k: adict(v) for k, v in data.items()})
    elif isinstance(data, list):
        return [adict(item) for item in data]
    else:
        return data
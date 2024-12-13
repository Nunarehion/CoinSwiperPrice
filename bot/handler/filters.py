from api.api_client import get_all_price
from bot.__init__ import *
state =  FilterMode()

# Инициализируем состояние пользователя, если его еще нет
user_state  = UserState()
def dataFilter(item, state) -> bool:
    match state.condition:
        case state.NEUTRAL:
            return item
        case state.POSITIVE:
            return item.percent >= user_state.minimum
        case state.NEGATIVE:
            return item.percent <= user_state.minimum

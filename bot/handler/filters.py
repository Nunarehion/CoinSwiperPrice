from api.api_client import get_all_price
from bot.__init__ import *

# Инициализируем состояние пользователя, если его еще нет
user_state  = UserState()
def dataFilter(item, filter_mode) -> bool:
    match filter_mode.condition:
        case filter_mode.NEUTRAL:
            return item
        case filter_mode.POSITIVE:
            return item.percent >= user_state.minimum
        case filter_mode.NEGATIVE:
            return item.percent <= user_state.minimum

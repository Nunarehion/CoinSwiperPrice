from api.api_client import get_all_price


def dataFilter(item, filter_mode, user_state) -> bool:
    match filter_mode.condition:
        case filter_mode.NEUTRAL:
            return item
        case filter_mode.POSITIVE:
            return item.percent >= user_state.minimum
        case filter_mode.NEGATIVE:
            return item.percent <= user_state.minimum

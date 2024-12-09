from datetime import datetime
from api.api_client import get_all_price
from bot.__init__ import *


def send_single_price_update(bot, chat_id):
    current_date = datetime.now().strftime("[Календарь] %d/%m/%Y")
    message = mk(current_date).code() + mk().indent()
    result = get_all_price()
    # Инициализируем состояние пользователя, если его еще нет
    if chat_id not in user_states:
        user_states[chat_id] = UserState()
    minimum = user_states[chat_id].minimum
    print(f"Текущее состояние user_states: {user_states}")
    print(f"Текущее состояние minimum: {minimum}")
    for coin in result:
        if coin.percent >= minimum:
            message += mk(f'{emoji.warning if coin.percent < minimum else emoji.accept} ') \
                - mk(f'({coin.percent}%) #{coin.token}').bold() \
                + mk(f'{coin.exchanges[0].name}: {coin.exchanges[0].price}$').mono().align() \
                - mk(f' ({round(float(coin.exchanges[0].gas_fee), 1) if coin.exchanges[0].gas_fee else "--.-"}$)').mono() \
                - emoji.up \
                + mk(f'{coin.exchanges[1].name}: {coin.exchanges[1].price}$').mono().align() \
                - mk(f' ({round(float(coin.exchanges[1].gas_fee), 1) if coin.exchanges[1].gas_fee else "--.-"}$)').mono() \
                - emoji.down \
                + mk(f'Спред: {round(float(coin.difference), 4)}$').bold() \
                + mk().indent()
        else:
             message += mk(f'{emoji.warning if coin.percent < minimum else emoji.accept} ') \
                - mk(f'({coin.percent}%) #{coin.token}').bold() \
                + mk(f'Не удовлетворяет условию') \
                + mk().indent()

    bot.send_message(chat_id, message, parse_mode='HTML')
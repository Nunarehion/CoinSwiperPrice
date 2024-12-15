from datetime import datetime
from api.api_client import get_all_price
from bot.__init__ import *
from bot.handler.filters import dataFilter
from bot.handler.button import *


def send_single_price_update(bot, chat_id):
    current_date = datetime.now().strftime("[Календарь] %d/%m/%Y")
    message = mk(current_date).code() + mk().indent()
    result = get_all_price()
    # Инициализируем состояние пользователя, если его еще нет
    if chat_id not in user_states:
        user_states[chat_id] = UserState()
    minimum = user_states[chat_id].minimum
    filter_mode = user_states[chat_id].filter_mode
    arr = []
    print(f"Текущее состояние user_states: {user_states}")
    print(f"Текущее состояние minimum: {minimum}")
    for coin in result:
            text = mk(f'{emoji.warning if coin.percent < minimum else emoji.accept} ') \
                - mk(f'({coin.percent}%) #{coin.token}').bold() \
                + mk(f'{coin.exchanges[0].name}: {coin.exchanges[0].price}$').mono().align() \
                - mk(f' ({round(float(coin.exchanges[0].gas_fee), 1) if coin.exchanges[0].gas_fee else "--.-"}$)').mono() \
                - emoji.up \
                + mk(f'{coin.exchanges[1].name}: {coin.exchanges[1].price}$').mono().align() \
                - mk(f' ({round(float(coin.exchanges[1].gas_fee), 1) if coin.exchanges[1].gas_fee else "--.-"}$)').mono() \
                - emoji.down \
                + mk(f'Спред: {round(float(coin.difference), 4)}$').bold() \
                + mk().indent()
            instance = CryptoPortfolio(percent=coin.percent, text=text)
            arr.append(instance)
    message += "".join([str(item.text) for item in arr if dataFilter(item, filter_mode)])

    keyboard = InlineKeyboardMarkup()

    if filter_mode.condition == filter_mode.NEUTRAL:
        keyboard.add(InlineKeyboardButton("Позитивный", callback_data='positive'))
        keyboard.add(InlineKeyboardButton("Негативный", callback_data='negative'))
    elif filter_mode.condition == filter_mode.POSITIVE:
        keyboard.add(InlineKeyboardButton("Нейтральный", callback_data='neutral'))
        keyboard.add(InlineKeyboardButton("Негативный", callback_data='negative'))
    elif filter_mode.condition == filter_mode.NEGATIVE:
         keyboard.add(InlineKeyboardButton("Нейтральный", callback_data='neutral'))
         keyboard.add(InlineKeyboardButton("Позитивный", callback_data='positive'))

    bot.send_message(chat_id, message, reply_markup=keyboard, parse_mode='HTML')
    message =  bot.send_message(chat_id, message, reply_markup=keyboard, parse_mode='HTML')
    message_id = message.message_id
    user_states[chat_id].cash[message_id] = arr

@bot.callback_query_handler(func=lambda call: True)
def button_handler(call: CallbackQuery):
    user_state = user_states[call.message.chat.id]
    filter_mode = user_state.filter_mode
    if call.data == 'positive':
        filter_mode.set_positive()
    elif call.data == 'negative':
        filter_mode.set_negative()
    elif call.data == 'neutral':
        filter_mode.set_neutral()

    send_single_price_update(bot, call.message.chat.id)
    bot.answer_callback_query(call.id)

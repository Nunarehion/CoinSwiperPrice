from datetime import datetime
from api.api_client import get_all_price
from bot.__init__ import *
from bot.handler.filters import dataFilter
from bot.handler.callback_price_button import *


def send_single_price_update(bot, chat_id):
    current_date = datetime.now().strftime("[Календарь] %d/%m/%Y")
    header = mk(current_date).code() + mk().indent()
    result = get_all_price()
    
    if chat_id not in user_states:
        user_states[chat_id] = UserState()
    minimum = user_states[chat_id].minimum
    filter_mode = user_states[chat_id].filter_mode
    
    arr_crypto = []
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
            instance = TextChunk(percent=coin.percent, text=text)
            arr_crypto.append(instance)
            
    cash_message = CashLargeMessage(header=header, messages=arr_crypto, filter_mode=filter_mode)
    
    filtered_message = cash_message.load_cash(user_states[chat_id])
    message = cash_message.header
    message += filtered_message
    
    keyboard = InlineKeyboardMarkup()
    if filter_mode.condition == filter_mode.NEUTRAL:
        keyboard.add(InlineKeyboardButton("Позитивный", callback_data= 'cash_' + filter_mode.POSITIVE))
        keyboard.add(InlineKeyboardButton("Негативный", callback_data= 'cash_' + filter_mode.NEGATIVE))
    elif filter_mode.condition == filter_mode.POSITIVE:
        keyboard.add(InlineKeyboardButton("Нейтральный", callback_data= 'cash_' + filter_mode.NEUTRAL))
        keyboard.add(InlineKeyboardButton("Негативный", callback_data= 'cash_' + filter_mode.NEGATIVE))
    elif filter_mode.condition == filter_mode.NEGATIVE:
         keyboard.add(InlineKeyboardButton("Нейтральный", callback_data= 'cash_' + filter_mode.NEUTRAL))
         keyboard.add(InlineKeyboardButton("Позитивный", callback_data= 'cash_' + filter_mode.POSITIVE))

    message =  bot.send_message(chat_id, message, reply_markup=keyboard, parse_mode='HTML')
    message_id = message.message_id
    
    user_states[chat_id].cash[message_id] = cash_message


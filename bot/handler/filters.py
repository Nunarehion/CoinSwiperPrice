
from bot.__init__ import *


@bot.message_handler(commands=['filters'])
def filters(message):
    text = (
        mk("Доступные режимы фильтрации:").indent() \
        + mk("1. Нейтральный: не влияет на результаты.").indent() \
        + mk("2. Позитивный: фильтрует положительные результаты.").indent() \
        + mk("3. Негативный: фильтрует отрицательные результаты.").indent() \
        + mk("Выберите режим фильтрации, нажав на соответствующую кнопку ниже:")
    )
    keyboard = InlineKeyboardMarkup()
    callbackGroup = "global_"
    keyboard.add(InlineKeyboardButton("Нейтральный", callback_data=  callbackGroup + FilterMode.NEUTRAL))
    keyboard.add(InlineKeyboardButton("Позитивный",  callback_data=  callbackGroup + FilterMode.POSITIVE))
    keyboard.add(InlineKeyboardButton("Негативный",  callback_data=  callbackGroup + FilterMode.NEGATIVE))
    
    bot.send_message(message.chat.id, text.code(), reply_markup=keyboard, parse_mode='HTML')
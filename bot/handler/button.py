from bot.__init__ import *
from bot.handler.filters import dataFilter
from datetime import datetime

user_states = {}  

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
    keyboard.add(InlineKeyboardButton("Нейтральный", callback_data='neutral'))
    keyboard.add(InlineKeyboardButton("Позитивный", callback_data='positive'))
    keyboard.add(InlineKeyboardButton("Негативный", callback_data='negative'))
    
    bot.send_message(message.chat.id, text.code(), reply_markup=keyboard, parse_mode='HTML')

@bot.callback_query_handler(func=lambda call: True)
def button_handler(call: CallbackQuery):
    chat_id = call.message.chat.id
    if chat_id not in user_states:
        user_states[chat_id] = UserState()
    filter_mode = user_states[chat_id].filter_mode
    if call.data == 'neutral':
        filter_mode.set_neutral()
    elif call.data == 'positive':
        filter_mode.set_positive()
    elif call.data == 'negative':
        filter_mode.set_negative()
    current_date = datetime.now().strftime("[Календарь] %d/%m/%Y")
    message = mk(current_date).code() + mk().indent()
    message += "".join([str(item.text) for item in user_states[chat_id].cash[call.message.message_id] if dataFilter(item, filter_mode)])

    bot.answer_callback_query(call.id) 
    bot.edit_message_text(text=message, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode='HTML', reply_markup=call.message.reply_markup)
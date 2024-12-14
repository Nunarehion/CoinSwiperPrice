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
    keyboard.add(InlineKeyboardButton("Нейтральный", callback_data='neutral'))
    keyboard.add(InlineKeyboardButton("Позитивный", callback_data='positive'))
    keyboard.add(InlineKeyboardButton("Негативный", callback_data='negative'))
    
    bot.send_message(message.chat.id, text.code(), reply_markup=keyboard, parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def button_handler(call: CallbackQuery):
    global filter_mode
    if call.data == 'neutral':
        filter_mode.set_neutral()
    elif call.data == 'positive':
        filter_mode.set_positive()
    elif call.data == 'negative':
        filter_mode.set_negative()

    bot.answer_callback_query(call.id) 
    bot.edit_message_text(text=f"Режим фильтрации установлен на: {filter_mode.condition}", chat_id=call.message.chat.id, message_id=call.message.message_id)
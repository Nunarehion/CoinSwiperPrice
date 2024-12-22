from bot.__init__ import *

@bot.message_handler(commands=['setmin'])
def set_min(message):
    user_id = message.from_user.id
    if user_id not in user_states:
        user_states[user_id] = UserState()

    user_state = user_states[user_id]
    text = message.text

    match = re.search(r'(\d+(\.\d+)?)', text)
    if match:
        user_state.minimum = float(match.group(1))
        bot.reply_to(message, mk(f"Минимальный процент установлен на {user_state.minimum}%.").code(), parse_mode='HTML')
        return

    if user_state.waiting_for_input:
        bot.reply_to(message, mk("Вы уже находитесь в режиме ввода. Пожалуйста, введите число.").code(), parse_mode='HTML')
        return

    user_state.waiting_for_input = True

    markup = types.InlineKeyboardMarkup()
    cancel_button = types.InlineKeyboardButton("Отмена", callback_data="cancel")
    markup.add(cancel_button)

    input_message = bot.send_message(message.chat.id, mk("Пожалуйста, введите минимальный процент:").code(), reply_markup=markup, parse_mode='HTML')
    user_state.input_message_id = input_message.message_id

    Timer(20, cancel_input, [message]).start()

@bot.message_handler(func=lambda message: message.from_user.id in user_states and user_states[message.from_user.id].waiting_for_input)
def handle_input(message):
    user_id = message.from_user.id
    user_state = user_states[user_id]
    text = message.text

    match = re.search(r'(\d+(\.\d+)?)', text)
    
    if match:
        user_state.minimum = float(match.group(1))
        bot.reply_to(message, mk(f"Минимальный процент установлен на {user_state.minimum}%.").code(), parse_mode='HTML')
        user_state.waiting_for_input = False
        if user_state.input_message_id:
            try:
                bot.delete_message(message.chat.id, user_state.input_message_id)
            except telebot.apihelper.ApiTelegramException:
                pass
        user_state.input_message_id = None
    else:
        bot.reply_to(message, mk("Пожалуйста, укажите корректный процент в формате 'число%'.").code(), parse_mode='HTML')
        user_state.waiting_for_input = False


def cancel_input(message):
    user_id = message.from_user.id
    if user_id in user_states:
        user_state = user_states[user_id]
        user_state.waiting_for_input = False
        if user_state.input_message_id:
            try:
                bot.delete_message(message.chat.id, user_state.input_message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения: {e}")
        user_state.input_message_id = None

@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def callback_cancel(call):
    cancel_input(call.message)
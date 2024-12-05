from bot.__init__ import *
from bot.utils import send_messages
from bot.utils import mk

@bot.message_handler(commands=['setmin'])
def set_min(message):
    global waiting_for_input, user_id_waiting, input_message_id
    text = message.text

    match = re.search(r'(\d+(\.\d+)?)', text)
    if match:
        minimum = float(match.group(1))
        bot.reply_to(message, f"Минимальный процент установлен на {minimum}%.")
        return

    if waiting_for_input:
        bot.reply_to(message, "Вы уже находитесь в режиме ввода. Пожалуйста, введите число.")
        return

    waiting_for_input = True
    user_id_waiting = message.from_user.id

    markup = types.InlineKeyboardMarkup()
    cancel_button = types.InlineKeyboardButton("Отмена", callback_data="cancel")
    markup.add(cancel_button)

    input_message = bot.send_message(message.chat.id, "Пожалуйста, введите минимальный процент:", reply_markup=markup)
    input_message_id = input_message.message_id

    Timer(10, cancel_input, [message]).start()

@bot.message_handler(func=lambda message: waiting_for_input and message.from_user.id == user_id_waiting)
def handle_input(message):
    global minimum, waiting_for_input, user_id_waiting, input_message_id
    text = message.text

    match = re.search(r'(\d+(\.\d+)?)', text)
    
    if match:
        minimum = float(match.group(1))
        bot.reply_to(message, f"Минимальный процент установлен на {minimum}%.")
        waiting_for_input = False
        user_id_waiting = None
        if input_message_id:
            try:
                bot.delete_message(message.chat.id, input_message_id)
            except telebot.apihelper.ApiTelegramException:
                pass
    else:
        bot.reply_to(message, "Пожалуйста, укажите корректный процент в формате 'число%'.")


def cancel_input(message):
    global waiting_for_input, user_id_waiting, input_message_id
    waiting_for_input = False
    user_id_waiting = None
    if input_message_id:
        bot.delete_message(message.chat.id, input_message_id)
        

@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def callback_cancel(call):
    cancel_input(call.message)
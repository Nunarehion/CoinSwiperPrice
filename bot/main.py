import api
import data.coins
import time
from api.api_client import get_all_price
from bot.classes import mk
from bot.handler.regular_symbol import escape_special
from bot.__init__ import *
from bot.utils import send_messages
from bot.handler.start import *
from bot.handler.stop import *
from bot.handler.exit import *

# coin = adict()
# coin.percent = 10
# coin.symbol = 'BTC'
# coin.list = [adict(name='uniswap', price=123),
#               adict(name='coinbase', price=121)]
# coin.difference = 3

# result = get_all_price()
# print(result)

  



import telebot
import time
import threading
import re
from datetime import datetime
from threading import Timer
from telebot import types






print("BOT START")







        


    



def cancel_input(message):
    global waiting_for_input, user_id_waiting, input_message_id
    waiting_for_input = False
    user_id_waiting = None
    if input_message_id:
        bot.delete_message(message.chat.id, input_message_id)

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

@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def callback_cancel(call):
    cancel_input(call.message)


@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = mk("Доступные команды:") \
        + mk().indent() \
        + mk("/start - Включить уведомления о изменениях цен на криптовалюты.") \
        + mk().indent() \
        + mk("При активации бот будет отправлять уведомления о текущих ценах и изменениях.") \
        + mk().indent() \
        + mk("/stop - Отключить уведомления.") \
        + mk().indent() \
        + mk("Используйте эту команду, чтобы остановить получение уведомлений.") \
        + mk().indent() \
        + mk("/setmin <число%> - Установить минимальный процент для уведомлений.") \
        + mk().indent() \
        + mk("Например, команда /setmin 10% установит минимальный процент на 10%.") \
        + mk().indent() \
        + mk("/help - Показать это сообщение с описанием команд.") \
        + mk().indent() \
        + mk("Этот бот отправляет уведомления о ценах на криптовалюты и их изменения.") \
        + mk().indent() \
        + mk("Используйте команду /setmin, чтобы установить минимальный процент, при котором бот будет отправлять уведомления.") \
        + mk().indent() \
        + mk("💡 Примечание: Убедитесь, что вы вводите процент в формате 'число%'.") \
        + mk().indent() \
        + mk("Если у вас есть вопросы или предложения, не стесняйтесь обращаться!")
    
    bot.reply_to(message, help_text.code(), parse_mode='MarkdownV2')

        
bot.set_my_commands([
    telebot.types.BotCommand("start", "Включить уведомления"),
    telebot.types.BotCommand("stop",  "Отключить уведомления"),
    telebot.types.BotCommand("help", "Справка"),
    telebot.types.BotCommand("setmin", "Задать минимальный процент"),
    telebot.types.BotCommand("options", "Настройка"),
    telebot.types.BotCommand("exit", "Выключить бота"),
])


settings = ["Настройка 2", "Настройка 2"]

@bot.message_handler(commands=['options'])
def send_poll(message):
    question = "Выберите настройки:"
    options = settings
    bot.send_poll(message.chat.id, question, options, is_anonymous=False, allows_multiple_answers=True)

@bot.poll_answer_handler(func=lambda answer: True)
def handle_poll_answer(answer):
    selected_options = answer.option_ids
    selected_settings = [settings[i] for i in selected_options]
    bot.send_message(answer.user.id, f"Выбранные настройки: {', '.join(selected_settings)}")


    

bot.polling()
import api
import data.coins
import time
from api.api_client import get_all_price
from bot.utils import mk
from bot.__init__ import *
from bot.utils import send_messages
from bot.handler.start import *
from bot.handler.stop import *
from bot.handler.exit import *
from bot.handler.help import *
from bot.handler.setmin import *


  



import telebot
import time
import threading
import re
from datetime import datetime
from threading import Timer
from telebot import types






print("BOT START")







        


    








        
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
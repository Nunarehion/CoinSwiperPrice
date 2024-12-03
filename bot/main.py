import api
import data.coins
import time
from api.api_client import get_all_price

from adict import adict

emoji = adict({'warning': '\U0001F7E5', 'accept': '\U0001F7E9', 'up': '\U0001F53A', 'down': '\U0001F53B'})
# coin = adict()
# coin.percent = 10
# coin.symbol = 'BTC'
# coin.list = [adict(name='uniswap', price=123),
#               adict(name='coinbase', price=121)]
# coin.difference = 3

# result = get_all_price()
# print(result)
class mk:
    def __init__(self, st='', escape='true'):
        if escape:
          st = st
        self.st = st
        
    def escape_markdown(self, text):
        print(text)
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in special_chars:
            text = text.replace(char, f'{char}')
        print(text)
        return text
        
    def indent(self, n = 1):
        self.st += '\n'
        return self

    def bold(self):
        self.st = f'***{self.st}***'
        return self
    
    def italic(self):
        self.st = f'_{self.st}_'
        return self
        
    def under(self):
        self.st = f'__{self.st}__'
        
    def mono(self):
        self.st = f'`{self.st}`'
        return self
        
    def code(self, language=''):
        self.st = f'```{language}\n{self.st}```'
        return self
        
    def align(self, width=9):
        parts = self.st.split(':')
        if len(parts) == 2:
            first_part_length = len(parts[0])
            spaces_to_add = max(0, width - first_part_length)
            self.st = f"{parts[0]}: {' ' * spaces_to_add}{parts[1].strip()}"
        return self

    def __repr__(self):
        return self.st
        
    def __add__(self, other):
        if isinstance(other, mk):
            return mk(self.st + '\n' + other.st)
        return mk(self.st + '\n' + str(other))

    def __radd__(self, other):
        return mk(str(other) + self.st)
        
    def __sub__(self, other):
        if isinstance(other, mk):
            return mk(self.st + other.st)
        return mk(self.st + str(other))
  



import telebot
import time
import threading
import re
from datetime import datetime
from threading import Timer
from telebot import types


API_TOKEN = '7116422869:AAG_j_sUrP6JGJ8IW2c38WWmWeDe6UcCd_A'
bot = telebot.TeleBot(API_TOKEN)


running = False
print("BOT START")

def escape_special(text):
    text = str(text)
    special_characters = r'[\^$.|?*+(){}[\]-]'

    escaped_text = re.sub(special_characters, r'\\\g<0>', text)
    return escaped_text

def send_messages(chat_id):
    global running
    global minimum
    while running:
        current_date = datetime.now().strftime("[Календарь] %d/%m/%Y")
        message = mk(current_date).code() + mk().indent()
        result = get_all_price()
        for coin in result:
            message += mk(f'{emoji.warning if coin.percent < minimum else emoji.accept} ') \
                - mk(f'\({escape_special(coin.percent)}\\%\) \#{coin.token}').bold() \
                + mk(f'{coin.exchanges[0].name}: {escape_special(coin.exchanges[0].price)}\$').mono().align() \
                - emoji.up\
                + mk(f'{coin.exchanges[1].name}: {escape_special(coin.exchanges[1].price)}\$').mono().align() \
                - emoji.down\
                + mk(f'Общая разница: {escape_special(coin.difference)}').bold()\
                + mk().indent()

        bot.send_message(chat_id, message, parse_mode='MarkdownV2')
        time.sleep(15)


@bot.message_handler(commands=['start'])
def start_command(message):
    global running
    if not running:
        bot.reply_to(message, mk("Уведомления включены.    ").mono(), parse_mode='MarkdownV2')
        running = True
        threading.Thread(target=send_messages, args=(message.chat.id,)).start()
        

@bot.message_handler(commands=['stop'])
def stop_command(message):
    global running
    running = False
    bot.reply_to(message, mk("Уведомления остановленны.    ").mono(), parse_mode='MarkdownV2')
    
    
minimum = 0.5
waiting_for_input = False
user_id_waiting = None

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

@bot.message_handler(commands=['exit'])
def exit(message):
    bot.reply_to(message, "Бот выключен")
    exit()
    

bot.polling()
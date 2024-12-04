from bot.__init__ import *
from bot.utils import send_messages

@bot.message_handler(commands=['start'])
def start_command(message):
    global running
    if not running:
        bot.reply_to(message, mk("Уведомления включены.    ").mono(), parse_mode='MarkdownV2')
        running_event.set()  # Устанавливаем событие
        threading.Thread(target=send_messages, args=(bot, message.chat.id, running, minimum)).start()
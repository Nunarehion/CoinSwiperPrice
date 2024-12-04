from bot.__init__ import *
from bot.utils import send_messages
@bot.message_handler(commands=['stop'])
def stop_command(message):
    global running
    running_event.clear()  # Устанавливаем событие
    bot.reply_to(message, mk("Уведомления остановленны.    ").mono(), parse_mode='MarkdownV2')
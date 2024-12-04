from bot.__init__ import *
import sys
from bot.utils import send_messages
@bot.message_handler(commands=['exit'])
def exit_bot(message):
    bot.reply_to(message, "Бот выключен")
    running_event.clear()  # Очищаем событие, чтобы остановить отправку сообщений
    time.sleep(1)  # Задержка, чтобы дать время на отправку сообщения
    bot.stop_polling()  # Останавливаем обработку сообщений
    sys.exit()  # Завершаем выполнение программы
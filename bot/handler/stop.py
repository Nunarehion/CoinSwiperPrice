from bot.__init__ import *
from bot.utils import send_messages
from bot.utils import mk

@bot.message_handler(commands=['stop'])
def stop_command(message):
    user_id = message.chat.id
    if user_id in user_states:
        user_state = user_states[user_id]
        user_state.running_event.clear()
        user_state.running = False
        bot.reply_to(message, mk("Уведомления остановлены.").mono(), parse_mode='HTML')
    else:
        bot.reply_to(message, mk("Уведомления не были включены.").mono(), parse_mode='HTML')
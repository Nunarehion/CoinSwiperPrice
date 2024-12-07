from bot.__init__ import *
from bot.utils import send_messages
from bot.utils import mk

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.chat.id

    if user_id not in user_states:
        user_states[user_id] = UserState()

    user_state = user_states[user_id]

    if not user_state.running:
        bot.reply_to(message, mk("Уведомления включены.").mono(), parse_mode='HTML')
        user_state.running_event.set()
        user_state.running = True
        threading.Thread(target=send_messages, args=(bot, user_id, user_state)).start()
    else:
        bot.reply_to(message, mk("Уведомления уже включены.").mono(), parse_mode='HTML')

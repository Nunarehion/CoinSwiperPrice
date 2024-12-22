from bot.__init__ import *
from bot.handler.send import polling_price_update

@bot.message_handler(commands=['push'])
def push_command(message):
    user_id = message.chat.id

    if user_id not in user_states:
        user_states[user_id] = UserState()

    user_state = user_states[user_id]

    if not user_state.running:
        bot.reply_to(message, mk("Уведомления включены.").mono(), parse_mode='HTML')
        user_state.running_event.set()
        user_state.running = True

        user_state.thread = threading.Thread(target=polling_price_update, args=(bot, user_id, user_state))
        user_state.thread.start()
    else:
        bot.reply_to(message, mk("Уведомления уже включены.").mono(), parse_mode='HTML')

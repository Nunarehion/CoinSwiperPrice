from bot.__init__ import *

@bot.message_handler(commands=['stop'])
def stop_command(message):
    user_id = message.chat.id
    if user_id in user_states:
        user_state = user_states[user_id]
        
        if user_state.running:
            user_state.running_event.clear()
            user_state.running = False
            if user_state.thread is not None:
                user_state.thread.join()
            
            bot.reply_to(message, mk("Уведомления остановлены.").mono(), parse_mode='HTML')
        else:
            bot.reply_to(message, mk("Уведомления уже остановлены.").mono(), parse_mode='HTML')
    else:
        bot.reply_to(message, mk("Уведомления не были включены.").mono(), parse_mode='HTML')
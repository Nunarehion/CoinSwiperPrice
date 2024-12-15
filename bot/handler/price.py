from bot.__init__ import *
from bot.handler.send import send_single_price_update
import time
import threading

active_users = set()

@bot.message_handler(commands=['price'])
def price_command(message):
    user_id = message.chat.id

    if user_id in active_users:
        bot.send_message(user_id, "Вы уже запросили цену. Пожалуйста, подождите.")
        return

    active_users.add(user_id)
    loading_message = bot.send_message(user_id, "Loading")
    stop_loading = False

    def update_loading_message() -> None:
        """Цикл анимации при загрузке данных"""
        loading_texts = [
                            "🌑 Loading.",
                            "🌒 Loading..",
                            "🌓 Loading...",
                            "🌔 Loading",
                            "🌕 Loading.",
                            "🌖 Loading..",
                            "🌗 Loading...",
                            "🌘 Loading"
                        ]
        while not stop_loading:
            for text in loading_texts:
                if stop_loading:
                    break
                bot.edit_message_text(chat_id=user_id, message_id=loading_message.message_id, text=text)
                time.sleep(0.5)
    user_state = user_states.get(user_id)
    if user_state is None:
        user_state = UserState()
        user_states[user_id] = user_state
    loader_thread = threading.Thread(target=update_loading_message)
    loader_thread.start()

    send_single_price_update(bot, user_id)

    stop_loading = True
    loader_thread.join()

    bot.delete_message(chat_id=user_id, message_id=loading_message.message_id)

    active_users.remove(user_id)

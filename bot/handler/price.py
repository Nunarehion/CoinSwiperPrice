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
    print('HENDLER PRICE')
    loading_message = bot.send_message(user_id, "Loading")
    
    stop_loading = False

    def update_loading_message():
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

    loader_thread = threading.Thread(target=update_loading_message)
    loader_thread.start()

    # Здесь вызываем функцию для получения цены
    send_single_price_update(bot, user_id)

    # Останавливаем поток обновления лоадера
    stop_loading = True
    loader_thread.join()

    # Удаляем сообщение о загрузке
    bot.delete_message(chat_id=user_id, message_id=loading_message.message_id)

    # Удаляем пользователя из активных
    active_users.remove(user_id)

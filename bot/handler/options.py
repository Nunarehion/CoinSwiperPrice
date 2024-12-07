from bot.__init__ import *


settings = ["Настройка 2", "Настройка 2"]

@bot.message_handler(commands=['options'])  # noqa: F821
def send_poll(message):
    question = "Выберите настройки:"
    options = settings
    bot.send_poll(message.chat.id, question, options, is_anonymous=False, allows_multiple_answers=True)  # noqa: F821

@bot.poll_answer_handler(func=lambda answer: True)  # noqa: F821
def handle_poll_answer(answer):
    selected_options = answer.option_ids
    selected_settings = [settings[i] for i in selected_options]
    bot.send_message(answer.user.id, f"Выбранные настройки: {', '.join(selected_settings)}")  # noqa: F821

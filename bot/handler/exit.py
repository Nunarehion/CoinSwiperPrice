from bot.__init__ import * # noqa: F403

@bot.message_handler(commands=['exit'])
def exit_bot(message):
    bot.reply_to(message, "Бот выключен")
    ex
    
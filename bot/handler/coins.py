from bot.__init__ import * # noqa: F403

def get_data() -> str:
    result: str = str()
    for coin in data.coins.coins_data:
        token, symbol = coin['address'], coin['symbol']
        result += mk(f"{symbol}:").bold() \
                + mk(f"{token}").mono().indent()
    return result

@bot.message_handler(commands=['coins'])
def handler_coins_info(message):
    text = mk("Список всех монет: ").bold().indent() \
         + get_data()
    bot.send_message(message.chat.id, text,  parse_mode='HTML')

    
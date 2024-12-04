# bot/utils.py
import time
from datetime import datetime
from api.api_client import get_all_price
from bot.classes import mk
from bot.handler.regular_symbol import escape_special

from bot.__init__ import *



def send_messages(bot, chat_id, running, minimum):
     while running_event.is_set():
        current_date = datetime.now().strftime("[Календарь] %d/%m/%Y")
        message = mk(current_date).code() + mk().indent()
        result = get_all_price()
        for coin in result:
            message += mk(f'{emoji.warning if coin.percent < minimum else emoji.accept} ') \
                - mk(f'\({escape_special(coin.percent)}\\%\) \#{coin.token}').bold() \
                + mk(f'{coin.exchanges[0].name}: {escape_special(coin.exchanges[0].price)}\$').mono().align() \
                - emoji.up\
                + mk(f'{coin.exchanges[1].name}: {escape_special(coin.exchanges[1].price)}\$').mono().align() \
                - emoji.down\
                + mk(f'Общая разница: {escape_special(coin.difference)}').bold()\
                + mk().indent()

        bot.send_message(chat_id, message, parse_mode='MarkdownV2')
        time.sleep(15)

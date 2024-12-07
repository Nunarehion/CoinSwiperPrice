# bot/utils.py
import time
from datetime import datetime
from api.api_client import get_all_price
from bot.__init__ import *

# send_price_updates
def send_messages(bot, chat_id, user_state):
    while user_state.running_event.is_set():
        current_date = datetime.now().strftime("[Календарь] %d/%m/%Y")
        message = mk(current_date).code() + mk().indent()
        result = get_all_price()
        for coin in result:
             message += mk(f'{emoji.warning if coin.percent < minimum else emoji.accept} ') \
                 - mk(f'({coin.percent}%) #{coin.token}').bold()\
                 + mk(f'{coin.exchanges[0].name}: { coin.exchanges[0].price }$' ).mono().align()\
                 - mk(f' ({round(float(coin.exchanges[0].gas_fee), 1) if coin.exchanges[0].gas_fee else  "--.-" }$)').mono()\
                 - emoji.up\
                 + mk(f'{coin.exchanges[1].name}: { coin.exchanges[1].price }$').mono().align()\
                 - mk(f' ({round(float(coin.exchanges[1].gas_fee), 1) if coin.exchanges[1].gas_fee else  "--.-"}$)').mono()\
                 - emoji.down\
                 + mk(f'Спред: {round(float(coin.difference), 4)}$').bold()\
                 + mk().indent()

        bot.send_message(chat_id, message, parse_mode='HTML')
        time.sleep(15)

def send_single_price_update(bot, chat_id):
    current_date = datetime.now().strftime("[Календарь] %d/%m/%Y")
    message = mk(current_date).code() + mk().indent()
    result = get_all_price()
    
    for coin in result:
        message += mk(f'{emoji.warning if coin.percent < minimum else emoji.accept} ') \
            - mk(f'({coin.percent}%) #{coin.token}').bold() \
            + mk(f'{coin.exchanges[0].name}: {coin.exchanges[0].price}$').mono().align() \
            - mk(f' ({round(float(coin.exchanges[0].gas_fee), 1) if coin.exchanges[0].gas_fee else "--.-"}$)').mono() \
            - emoji.up \
            + mk(f'{coin.exchanges[1].name}: {coin.exchanges[1].price}$').mono().align() \
            - mk(f' ({round(float(coin.exchanges[1].gas_fee), 1) if coin.exchanges[1].gas_fee else "--.-"}$)').mono() \
            - emoji.down \
            + mk(f'Спред: {round(float(coin.difference), 4)}$').bold() \
            + mk().indent()

    bot.send_message(chat_id, message, parse_mode='HTML')



class mk:
    def __init__(self, st='', escape=True):
        self.st: str = st
        
    def indent(self, n=1):
        self.st += '\n'
        return self

    def bold(self):
        self.st = f'<b>{self.st}</b>'
        return self
    
    def italic(self):
        self.st = f'<i>{self.st}</i>'
        return self
        
    def under(self):
        self.st = f'<u>{self.st}</u>'
        return self
        
    def mono(self) -> str:
        self.st =  f"<code>{self.st}</code>"
        return self
        
    def code(self, language=''):
        self.st = f'<pre><code>{self.st}</code></pre>'
        return self
        
    def align(self, width=9):
        parts = self.st.split(':')
        if len(parts) == 2:
            first_part_length = len(parts[0])
            spaces_to_add = max(0, width - first_part_length)
            self.st = f"{parts[0]}: {' ' * spaces_to_add}{parts[1].strip()}"
        return self

    def __repr__(self):
        return self.st
        
    def __add__(self, other):
        if isinstance(other, mk):
            return mk(self.st + '\n' + other.st)
        return mk(self.st + '\n' + str(other))

    def __radd__(self, other):
        return mk(str(other) + self.st)
        
    def __sub__(self, other):
        if isinstance(other, mk):
            return mk(self.st + other.st)
        return mk(self.st + str(other))

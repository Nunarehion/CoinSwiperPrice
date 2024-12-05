# bot/utils.py
import time
from datetime import datetime
from api.api_client import get_all_price
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
                - mk(f'{escape_special(coin.exchanges[0].gas_fee) if coin.exchanges[0].gas_fee != None else "     "}')\
                - emoji.up\
                + mk(f'{coin.exchanges[1].name}: {escape_special(coin.exchanges[1].price)}\$').mono().align() \
                - mk(f'{escape_special(coin.exchanges[0].gas_fee) if coin.exchanges[1].gas_fee != None else "     "}')\
                - emoji.down\
                + mk(f'Общая разница: {escape_special(coin.difference)}').bold()\
                + mk().indent()

        bot.send_message(chat_id, message, parse_mode='MarkdownV2')
        time.sleep(15)

import re

def escape_special(text):
    text = str(text)
    # Все специальные символы для MarkdownV2
    special_characters = r'[_*[\]()~`>#+\-=|{}.!]'
    
    # Экранируем специальные символы
    escaped_text = re.sub(special_characters, r'\\\g<0>', text)
    
    return escaped_text
class mk:
    def __init__(self, st='', escape='true'):
        if escape:
          st = st
        self.st = st
        
    def escape_markdown(self, text):
        print(text)
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in special_chars:
            text = text.replace(char, f'{char}')
        print(text)
        return text
        
    def indent(self, n = 1):
        self.st += '\n'
        return self

    def bold(self):
        self.st = f'***{self.st}***'
        return self
    
    def italic(self):
        self.st = f'_{self.st}_'
        return self
        
    def under(self):
        self.st = f'__{self.st}__'
        
    def mono(self):
        self.st = f'`{self.st}`'
        return self
        
    def code(self, language=''):
        self.st = f'```{language}\n{self.st}```'
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
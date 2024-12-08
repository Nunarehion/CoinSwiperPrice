import time
from bot.__init__ import *
from . import send_single_price_update

def polling_price_update(bot, chat_id, user_state):
    while user_state.running_event.is_set():
        send_single_price_update(bot, chat_id)
        time.sleep(user_state.time_delay)
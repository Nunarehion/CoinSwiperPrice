import telebot
from telebot import types, apihelper
import threading
from threading import Timer 
from adict import adict
from dataclasses import dataclass
from utils import mk
import data.coins
import re



emoji = adict({'warning': '\U0001F7E5', 'accept': '\U0001F7E9', 'up': '\U0001F53A', 'down': '\U0001F53B'})

API_TOKEN = '7116422869:AAG_j_sUrP6JGJ8IW2c38WWmWeDe6UcCd_A'
bot = telebot.TeleBot(API_TOKEN)


@dataclass
class UserState:
    running: bool = False
    minimum: float = 0.5 #минимальный процент разницы устанавлеммый пользователем для индикаоров
    time_delay: int = 30 #временная задержка при отправке множества сообщений.
    waiting_for_input: bool = False
    user_id_waiting: str = None
    running_event: threading.Event = threading.Event()
    
user_states = {}
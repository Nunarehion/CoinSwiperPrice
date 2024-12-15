import telebot
from telebot import types, apihelper
import threading
from threading import Timer 
from adict import adict
from dataclasses import dataclass, field
from utils import mk
import data.coins
import re
from typing import List
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


emoji = adict({'warning': '\U0001F7E5', 'accept': '\U0001F7E9', 'up': '\U0001F53A', 'down': '\U0001F53B'})

API_TOKEN = '7116422869:AAG_j_sUrP6JGJ8IW2c38WWmWeDe6UcCd_A'
bot = telebot.TeleBot(API_TOKEN)


    


@dataclass
class CryptoPortfolio:
    percent: float
    text: str
@dataclass
class FilterMode:
    NEUTRAL: str = 'neutral'
    POSITIVE: str = 'positive'
    NEGATIVE: str = 'negative'
    condition: str = NEUTRAL
    def set_neutral(self):
        self.condition = self.NEUTRAL
    def set_positive(self):
        self.condition = self.POSITIVE
    def set_negative(self):
        self.condition = self.NEGATIVE


@dataclass
class UserState:
    running: bool = False
    minimum: float = 0.5 #минимальный процент разницы устанавлеммый пользователем для индикаоров
    time_delay: int = 30 #временная задержка при отправке множества сообщений.
    waiting_for_input: bool = False
    user_id_waiting: str = None
    filter_mode: FilterMode = field(default_factory=FilterMode)
    running_event: threading.Event = threading.Event()

user_states = {}
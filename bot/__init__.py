import telebot
from telebot import types, apihelper
import threading
from threading import Timer 
from adict import adict
from dataclasses import dataclass, field
from utils import mk
import data.coins
from copy import deepcopy
import re
from typing import List, Dict
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


emoji = adict({'warning': '\U0001F7E5', 'accept': '\U0001F7E9', 'up': '\U0001F53A', 'down': '\U0001F53B'})

API_TOKEN = '7116422869:AAG_j_sUrP6JGJ8IW2c38WWmWeDe6UcCd_A'
bot = telebot.TeleBot(API_TOKEN)


    
from dataclasses import field, dataclass
from typing import List, Dict, NewType
import threading
from copy import deepcopy

############################
"""Section FUNCTION UTILS"""
############################
def dataFilter(item, filter_mode, user_state) -> bool:
    match filter_mode.condition:
        case filter_mode.NEUTRAL:
            return item
        case filter_mode.POSITIVE:
            return item.percent >= user_state.minimum
        case filter_mode.NEGATIVE:
            return item.percent < user_state.minimum

###################
"""Section TYPES"""
###################
UserID = NewType('UserID', str)
MessageID = NewType('MessageID', str)

#####################
"""Section MODELS"""
#####################
@dataclass
class FilterMode:
    '''Модель предназначена для управлением состояний фильтра'''
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
    '''Модель предназначения для хранения пользовательских состояний'''
    minimum: float = 0.5 #%
    time_delay: int = 60 
    waiting_for_input: bool = False
    user_id_waiting: str = None
    cash: Dict[MessageID, dict] = field(default_factory=dict)
    filter_mode: FilterMode = field(default_factory=FilterMode)
    running: bool = False
    running_event: threading.Event = threading.Event()
    thread: threading.Thread = None 

@dataclass
class TextChunk:
    '''модель предназначена для хранения части сообщения'''
    percent: float
    text: str
    
@dataclass
class CashLargeMessage:
    '''модель предназначена для хранения состовных сообщений'''
    messages: List[TextChunk] = field(default_factory=list)
    filter_mode: FilterMode = field(default_factory=FilterMode)
    header: str = ''
    def __post_init__(self):
        if isinstance(self.filter_mode, FilterMode):
            self.filter_mode = deepcopy(self.filter_mode)
            
    def load_cash(self, user_state) -> str:
        return "".join([str(item.text) for item in self.messages if dataFilter(item, self.filter_mode, user_state)])

    
#####################
"""Section STORAGE"""
#####################
user_states: Dict[UserID, UserState] = {}


###############
"""Final MAP"""
###############
"""
user_states: Dict[UserID, UserState]
  └── UserState
        ├── running: bool
        ├── minimum: float
        ├── time_delay: int
        ├── waiting_for_input: bool
        ├── user_id_waiting: str
        ├── filter_mode: FilterMode
        │     ├── NEUTRAL: str
        │     ├── POSITIVE: str
        │     ├── NEGATIVE: str
        │     └── condition: str
        ├── running_event: threading.Event
        └── cash: Dict[MessageID, CashLargeMessage]
              └── CashLargeMessage
                      ├── messages: List[TextChunk]
                      │     ├── TextChunk
                      │     │     ├── filter_value: float
                      │     │     └── text: str
                      └── filter_mode: FilterMode
"""
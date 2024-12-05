import telebot
import time
import threading
import re
from datetime import datetime
from threading import Timer
from telebot import types
import api
import data.coins
import time
from api.api_client import get_all_price

from adict import adict

emoji = adict({'warning': '\U0001F7E5', 'accept': '\U0001F7E9', 'up': '\U0001F53A', 'down': '\U0001F53B'})


import telebot
API_TOKEN = '7116422869:AAG_j_sUrP6JGJ8IW2c38WWmWeDe6UcCd_A'
bot = telebot.TeleBot(API_TOKEN)

running = False
minimum = 0.5
waiting_for_input = False
user_id_waiting = None
running_event = threading.Event()
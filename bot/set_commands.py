from telebot import types
from bot import *  # noqa: F403
def set_my_commands() -> None:
    """Описание команд в меню бота"""
    bot.set_my_commands([  # noqa: F405, F821
        types.BotCommand("price", "Получить уведомления"),
        types.BotCommand("stop",  "Отключить уведомления"),
        types.BotCommand("start", "Включить уведомления"),
        types.BotCommand("help", "Справка"),
        types.BotCommand("setmin", "Задать минимальный процент"),
        types.BotCommand("options", "Настройка"),
        types.BotCommand("exit", "Выключить бота"),
    ])
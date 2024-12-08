from bot.handler.price import *  # noqa: F403
from bot.handler.start import *  # noqa: F403
from bot.handler.stop import *  # noqa: F403
from bot.handler.exit import *  # noqa: F403
from bot.handler.help import *  # noqa: F403
from bot.handler.setmin import *  # noqa: F403

from bot.set_commands import set_my_commands

def bot_init():
    print("BOT START")      
    set_my_commands()
    bot.polling()
    
if __name__ == '__main__':
    bot_init()
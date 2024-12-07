from api.api_client import get_all_price
from bot.utils import mk


from bot.utils import send_messages
from bot.handler.start import *  # noqa: F403
from bot.handler.stop import *  # noqa: F403
from bot.handler.exit import *  # noqa: F403
from bot.handler.help import *  # noqa: F403
from bot.handler.setmin import *  # noqa: F403

from bot.set_commands import set_my_commands

print("BOT START")
        
set_my_commands()
bot.polling()
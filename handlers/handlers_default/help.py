from loader import bot
from config_data.config import DEFAULT_COMMANDS
from keyboards.reply.reply_keyboards import EMPTY


@bot.message_handler(commands=["help"])
def bot_help(message):
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    text.insert(0, f"*Команды:*")
    bot.reply_to(message, "\n".join(text), parse_mode='Markdown', reply_markup=EMPTY)

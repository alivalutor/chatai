from loader import bot
from keyboards.reply.reply_keyboards import EMPTY


@bot.message_handler(commands=["start"])
def bot_start(message):
    bot.reply_to(message, f"Привет, {message.from_user.full_name}! Выберите команду:", reply_markup=EMPTY)

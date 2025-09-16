import requests
import time
from telebot import TeleBot
from api import gemini
from google.api_core.exceptions import ServiceUnavailable, BadRequest, Unauthenticated
from config_data.config import BOT_TOKEN
from services.chat_context import context_for_ai
from services.user_check import is_user_allowed

assert BOT_TOKEN is not None, "BOT_TOKEN должен быть инициализирован и иметь значение!"

bot = TeleBot(BOT_TOKEN)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if not is_user_allowed(message.from_user.id):
        bot.reply_to(message, "Извините, у вас нет доступа к этому боту.")
        return

    max_retries = 3
    delay = 5

    thinking_message = bot.send_message(message.chat.id, "ИИ готовит ответ...")
    bot.send_chat_action(message.chat.id, "typing")

    history_context = context_for_ai(message.from_user.id, message.text)
    result = gemini.request_ai(message.from_user.id, history_context)

    bot.delete_message(thinking_message.chat.id, thinking_message.message_id)

    for attempt in range(max_retries):
        try:
            for part in result:
                bot.send_message(message.chat.id, part, parse_mode="Markdown")
            break
        except ServiceUnavailable:
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
            else:
                bot.reply_to(message, "ИИ перегружен, попробуй позже.")
        except Exception as e:
            bot.reply_to(message, f"Ошибка при отправке сообщения от ИИ:'\n'{str(e)}")
            break


if __name__ == "__main__":
    print("Бот chatai запущен...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=60)
        except requests.exceptions.ReadTimeout:
            print("Произошёл таймаут чтения, повторная попытка через 5 секунд...")
            time.sleep(5)
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            time.sleep(5)

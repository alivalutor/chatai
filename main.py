import requests
from telebot import TeleBot
import time
from config_data.config import BOT_TOKEN
from api import gemini
from services.user_check import is_user_allowed

assert BOT_TOKEN is not None, "BOT_TOKEN должен быть инициализирован и иметь значение!"

bot = TeleBot(BOT_TOKEN)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if not is_user_allowed(message.from_user.id):
        bot.reply_to(message, "Извините, у вас нет доступа к этому боту.")
        return
    result = gemini.request_ai(message.text)
    try:
        for part in result:
            bot.send_message(message.chat.id, part, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"Ошибка при запросе к ИИ: {str(e)}")


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

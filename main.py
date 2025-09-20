import requests
import time
from loader import bot
import handlers

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

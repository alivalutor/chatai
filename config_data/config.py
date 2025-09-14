import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к. отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

OPENROUTER_TOKEN = os.getenv('OPENROUTER_TOKEN')
assert OPENROUTER_TOKEN is not None, 'OPENROUTER_TOKEN должен быть инициализирован и иметь определённое значение!'

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

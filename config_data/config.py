import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к. отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# OPENROUTER_TOKEN = os.getenv('OPENROUTER_TOKEN')

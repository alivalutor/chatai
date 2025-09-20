from telebot import TeleBot
from google import genai
from config_data import config


assert (
    config.BOT_TOKEN is not None
), "BOT_TOKEN должен быть инициализирован и иметь значение!"

bot = TeleBot(token=config.BOT_TOKEN)

client = genai.Client()

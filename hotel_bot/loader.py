from config_data import config
from telebot import TeleBot
from telebot.storage import StateMemoryStorage

storage = StateMemoryStorage()
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
headers = {
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com",
    "X-RapidAPI-Key": config.RAPID_API_KEY
}

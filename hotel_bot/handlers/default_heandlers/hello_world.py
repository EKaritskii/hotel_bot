from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['hello_world'])
def bot_hello_world(message: Message):
    bot.send_message(message.from_user.id,'привет мир')


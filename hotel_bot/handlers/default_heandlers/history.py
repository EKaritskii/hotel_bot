from loader import bot
from telebot.types import Message
import rapid_api
from rapid_api.history_com import hist_write


@bot.message_handler(commands=['history'])
def bot_history(message: Message):
    hist_write(message.from_user.id, message.chat.id)




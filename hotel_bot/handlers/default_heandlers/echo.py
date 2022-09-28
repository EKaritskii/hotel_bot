from loader import bot
from telebot.types import Message


@bot.message_handler(state=None)
def bot_echo(message: Message):
    if message.text.lower() == 'привет':
        bot.send_message(message.from_user.id, "Привет!")
    else:
        bot.reply_to(message, "Эхо без состояния или фильтра.\nСообщение:"
                     f"{message.text}")

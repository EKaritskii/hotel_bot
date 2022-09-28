from loader import bot
from telebot.types import Message
from states.hotel_req import Hotel_Req_State
from rapid_api.history_com import hist_add
import rapid_api


@bot.message_handler(commands=['lowprice'])
def bot_low_price(message: Message):
    bot.set_state(message.from_user.id, Hotel_Req_State.loc, message.chat.id)
    hist_add(message.from_user.id, message.chat.id, message.text)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['mode'] = 'low'
    bot.send_message(message.from_user.id, "Введите город!")


@bot.message_handler(commands=['highprice'])
def bot_high(message: Message):
    bot.set_state(message.from_user.id, Hotel_Req_State.loc, message.chat.id)
    hist_add(message.from_user.id, message.chat.id, message.text)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['mode'] = 'high'
    bot.send_message(message.from_user.id, "Введите город!")


@bot.message_handler(commands=['bestdeal'])
def bot_best(message: Message):
    bot.set_state(message.from_user.id, Hotel_Req_State.loc, message.chat.id)
    hist_add(message.from_user.id, message.chat.id, message.text)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['mode'] = 'best'
    bot.send_message(message.from_user.id, "Введите город!")



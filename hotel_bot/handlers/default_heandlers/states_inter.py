from loader import bot
from telebot.types import Message, CallbackQuery
from states.hotel_req import Hotel_Req_State
from rapid_api.big_piece import get_1
from telegram_bot_calendar import DetailedTelegramCalendar
from handlers.default_heandlers.cal import get_calendar, ALL_STEPS
from datetime import date, timedelta


@bot.message_handler(state=Hotel_Req_State.loc)
def max_hotels(message):
    bot.reply_to(message, "Введите сколько гостиниц нужно максимум!")
    bot.set_state(message.from_user.id, Hotel_Req_State.max_hotel, message.chat.id)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['loc'] = message.text


@bot.message_handler(state=Hotel_Req_State.max_hotel)
def photo_yes_no(message):
    if message.text.isdigit():
        bot.reply_to(message, "Нужно выводить фотографии да/нет?")
        bot.set_state(message.from_user.id, Hotel_Req_State.photo_req, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['max_hotel'] = message.text
    else:
        bot.reply_to(message, "Кол-во может содержать только цифры!")


@bot.message_handler(state=Hotel_Req_State.photo_req)
def photo_how_much(message):
    if message.text == 'да':
        bot.reply_to(message, "Сколько фото?")
        bot.set_state(message.from_user.id, Hotel_Req_State.photo, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo_req'] = message.text
    elif message.text == 'нет':

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo_req'] = message.text
            data['photo'] = 0
            if data['mode'] != 'best':
                data['highest'] = ''
                data['lowest'] = ''
                calendar_command(message)
            else:
                bot.send_message(message.from_user.id, "Введите нижний диапазон цен!")
                bot.set_state(message.from_user.id, Hotel_Req_State.lowest, message.chat.id)
    else:
        bot.send_message(message.from_user.id, "Не корректный ответ!")


@bot.message_handler(state=Hotel_Req_State.photo)
def photo_num_check(message):
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['photo'] = message.text
            mode = data['mode']
        if mode != 'best':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['highest'] = ''
                data['lowest'] = ''
            calendar_command(message)
        else:
            bot.send_message(message.from_user.id, "Введите нижний диапазон цен!")
            bot.set_state(message.from_user.id, Hotel_Req_State.lowest, message.chat.id)
    else:
        bot.reply_to(message, "Кол-во может содержать только цифры!")


@bot.message_handler(state=Hotel_Req_State.lowest)
def photo_highest(message):
    if message.text.isdigit():
        bot.reply_to(message, "Введите верхний диапазон цен!")
        bot.set_state(message.from_user.id, Hotel_Req_State.highest, message.chat.id)

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['lowest'] = message.text
    else:
        bot.reply_to(message, "Цена может содержать только цифры!")


@bot.message_handler(state=Hotel_Req_State.highest)
def photo_highest(message):
    if message.text.isdigit():

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['highest'] = message.text
        calendar_command(message)
    else:
        bot.reply_to(message, "Цена может содержать только цифры!")


def calendar_command(message: Message) -> None:
    today = date.today()
    calendar, step = get_calendar(calendar_id=1,
                                  current_date=today,
                                  min_date=today,
                                  max_date=today + timedelta(days=365),
                                  locale="ru")
    bot.set_state(message.from_user.id, Hotel_Req_State.check_in, message.chat.id)
    bot.send_message(message.from_user.id, f"Привет, Выбери {ALL_STEPS[step]} заезда", reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def handle_arrival_date(call: CallbackQuery):
    today = date.today()
    result, key, step = get_calendar(calendar_id=1,
                                     current_date=today,
                                     min_date=today,
                                     max_date=today + timedelta(days=365),
                                     locale="ru",
                                     is_process=True,
                                     callback_data=call)
    if not result and key:
        bot.edit_message_text(f"Выберите {ALL_STEPS[step]}",
                              call.from_user.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['check_in'] = result

            bot.edit_message_text(f"Дата заезда {result}",
                                  call.message.chat.id,
                                  call.message.message_id)

            bot.send_message(call.from_user.id, "Выберите дату выезда")
            calendar, step = get_calendar(calendar_id=2,
                                          min_date=result + timedelta(days=1),
                                          max_date=result + timedelta(days=365),
                                          locale="ru",
                                          )

            bot.send_message(call.from_user.id,
                             f"Выберите {ALL_STEPS[step]}",
                             reply_markup=calendar)

            bot.set_state(call.from_user.id, Hotel_Req_State.check_out, call.message.chat.id)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def handle_arrival_date_(call: CallbackQuery):
    today = date.today()
    result, key, step = get_calendar(calendar_id=2,
                                     current_date=today,
                                     min_date=today,
                                     max_date=today + timedelta(days=365),
                                     locale="ru",
                                     is_process=True,
                                     callback_data=call)
    if not result and key:
        bot.edit_message_text(f"Выберите {ALL_STEPS[step]}",
                              call.from_user.id,
                              call.message.message_id,
                              reply_markup=key)
    elif result:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['check_out'] = result

            bot.edit_message_text(f"Дата выезда {result}",
                                  call.message.chat.id,
                                  call.message.message_id)
        get_1(call)

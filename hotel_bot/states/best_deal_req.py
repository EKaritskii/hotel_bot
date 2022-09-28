from telebot.handler_backends import State, StatesGroup


class Best_deal_req(StatesGroup):
    loc = State()
    max_hotel = State()
    photo_req = State()
    photo = State()
    checkin = State()
    checkout = State()
    highest = State()
    lowest = State()



from telebot.handler_backends import State, StatesGroup


class Hotel_Req_State(StatesGroup):
    mode = State()
    loc = State()
    max_hotel = State()
    photo_req = State()
    photo = State()
    lowest = State()
    highest = State()
    check_in = State()
    check_out = State()




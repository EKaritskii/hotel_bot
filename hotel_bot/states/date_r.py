from telebot.handler_backends import State, StatesGroup


class DateRangeState(StatesGroup):
    check_in = State()
    check_out = State()

from telebot.handler_backends import State, StatesGroup


class StudentReg(StatesGroup):
    first_name = State()
    last_name = State()
    address = State()
    age = State()
    phone = State()
    course = State()
    language = State()

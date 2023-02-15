from api_priv import student_reg_io
from telebot import TeleBot, storage
from msg_text import start_msg, send_firstname_msg, send_lastname_msg, send_address_msg, send_age_msg, phone_number_msg, \
    course_send_msg, course_lang_msg
from states import StudentReg
from keyboard import share_button_number, button_lang_inline

API_TOKEN = student_reg_io()

state_stg = storage.StateMemoryStorage()
bot = TeleBot(API_TOKEN, state_storage=state_stg)


# msg = Message; storage = stg
@bot.message_handler(commands=['start'])
def welcome_msg(message):
    bot.reply_to(message, start_msg(message.from_user.first_name))


@bot.message_handler(commands=['reg'])
def reg_steps_first_name(message):
    print(message)
    bot.send_message(message.chat.id, send_firstname_msg)  # First Name
    bot.set_state(message.from_user.id, StudentReg.first_name, message.chat.id)


@bot.message_handler(state=StudentReg.first_name)
def reg_steps_last_name(message):
    print(message)
    bot.send_message(message.chat.id, send_lastname_msg)  # Last Name
    bot.set_state(message.from_user.id, StudentReg.last_name, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as date:
        date['first_name'] = message.text


@bot.message_handler(state=StudentReg.last_name)
def reg_steps_address(message):
    bot.send_message(message.chat.id, send_address_msg)  # Address
    bot.set_state(message.from_user.id, StudentReg.address, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as date:
        date['last_name'] = message.text


@bot.message_handler(state=StudentReg.address)
def reg_steps_age(message):
    bot.send_message(message.chat.id, send_age_msg)  # Age
    bot.set_state(message.from_user.id, StudentReg.age, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as date:
        date['address'] = message.text


@bot.message_handler(state=StudentReg.age, content_types=['contact'])
def reg_steps_age(message):
    bot.send_message(message.chat.id, phone_number_msg, reply_markup=share_button_number)  # Phone
    bot.set_state(message.from_user.id, StudentReg.phone, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as date:
        date['phone'] = message.text


@bot.message_handler(state=StudentReg.course)
def reg_steps_age(message):
    bot.send_message(message.chat.id, course_send_msg)  # Course
    bot.set_state(message.from_user.id, StudentReg.course, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as date:
        date['course'] = message.text


@bot.message_handler(commands=['lang'])
def reg_steps_age(message):
    bot.send_message(message.chat.id, course_lang_msg, reply_markup=button_lang_inline)  # Course Lang
    bot.set_state(message.from_user.id, StudentReg.language, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as date:
        date['language'] = message.text


@bot.callback_query_handler(lambda call: call.data.startswith("language_"), state=StudentReg.language)
def reg_step_lang(call):
    message = call.message
    lang_code = call.data.split('_')[2]


if __name__ == '__main__':
    print('Worked:')
    bot.polling()

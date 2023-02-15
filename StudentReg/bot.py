from api_priv import student_reg_io
from telebot import TeleBot
import messages
import buttons
import utils

API_TOKEN = student_reg_io()
bot = TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def welcome_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, messages.START_MSG)


@bot.message_handler(commands=['reg'])
def reg_student(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, messages.FIRST_NAME)
    bot.register_next_step_handler(msg, first_name)


user_info = {}


def first_name(message):
    chat_id = message.chat.id
    user_info['First_Name'] = message.text
    msg = bot.send_message(chat_id, messages.LAST_NAME)
    bot.register_next_step_handler(msg, last_name)


def last_name(message):
    chat_id = message.chat.id
    user_info['Last_Name'] = message.text
    msg = bot.send_message(chat_id, messages.AGE)
    bot.register_next_step_handler(msg, get_age)


def get_age(message):
    chat_id = message.chat.id
    user_info['Age'] = message.text
    msg = bot.send_message(chat_id, messages.ADDRESS)
    bot.register_next_step_handler(msg, address_user)


def address_user(message):
    chat_id = message.chat.id
    user_info['Address'] = message.text
    msg = bot.send_message(chat_id, messages.COURSE_, reply_markup=buttons.course_buttons)
    bot.register_next_step_handler(msg, course_user)


@bot.callback_query_handler(lambda call: call.data.startswith('course_'))
def course_user(call):
    message = call.message
    course = call.data.split('_')[1]
    user_info['Course'] = course
    msg = bot.send_message(message.chat.id, messages.LANG_COURSE, reply_markup=buttons.language_buttons)
    bot.register_next_step_handler(msg, course_lang)


@bot.callback_query_handler(lambda call: call.data.startswith('lang_'))
def course_lang(call):
    message = call.message
    lang_course = call.data.split('_')[1]
    user_info['Language'] = lang_course
    msg = bot.send_message(message.chat.id, messages.TIME_COURSE, reply_markup=buttons.time_buttons)
    bot.register_next_step_handler(msg, time__course)


@bot.callback_query_handler(lambda call: call.data.startswith('time_'))
def time__course(call):
    message = call.message
    time_user = call.data.split('_')[1]
    if time_user == '09':
        time_user = '09:00'
    elif time_user == '15':
        time_user = '15:00'
    else:
        time_user = '19:00'
    user_info['Time'] = time_user
    user_first_name = user_info.get('First_Name')
    user_last_name = user_info.get('Last_Name')
    user_age = user_info.get('Age')
    user_address = user_info.get('Address')
    user_course = user_info.get('Course')
    user_lang = user_info.get('Language')
    user_time = user_info.get('Time')
    bot.send_message(message.chat.id,
                     messages.info_user_full(user_first_name, user_last_name, user_age, user_address, user_course,
                                             user_lang, user_time), reply_markup=buttons.confirm_buttons)


@bot.callback_query_handler(lambda call: call.data.startswith('answer_'))
def confirm(call):
    message = call.message
    answer = call.data.split('_')[1]
    if answer == 'yes':
        utils.write_dict_to_csv(user_info, 'user.csv')
        bot.send_message(message.chat.id, 'Saved!\n ')
    elif answer == 'no':
        user_info.clear()
        bot.send_message(message.chat.id, 'Send /start command')
        user_info.clear()
    else:
        bot.send_message(message.chat.id, 'oops!\nWrong Answer Send /start')


if __name__ == '__main__':
    print('Worked! @StudentReg_ioBot')
    bot.polling()

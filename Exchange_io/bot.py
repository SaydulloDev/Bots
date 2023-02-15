from api_priv import exchange_io
from api_request import get_user_request
from json_read import json_api_reader
from buttons_ex import currency_button_inline, DICT_CURRENCY, currency_button_inline2
from msg_bot import start_user_msg
from telebot import TeleBot

API_TOKEN = exchange_io()
bot = TeleBot(API_TOKEN, parse_mode='html')


# msg = message
@bot.message_handler(commands=['start'])
def welcome_msg(message):
    chat_id = message.chat.id
    user = message.from_user
    bot.send_message(chat_id, start_user_msg(user.first_name))


@bot.message_handler(commands=['exchange'])
def exchange_currency(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Select Currency👇', reply_markup=currency_button_inline)


currency_list = []


@bot.callback_query_handler(lambda call: call.data.startswith('currency_'))
def in_currency(call):
    message = call.message
    selected_currency = DICT_CURRENCY.get(call.data[-3::])
    currency_list.append(selected_currency)
    bot.send_message(message.chat.id, f"You Selected {selected_currency}\nSelect the Currency to exchange💱",
                     reply_markup=currency_button_inline2)


@bot.callback_query_handler(lambda call: call.data.startswith('to_currency_'))
def to_exchange(call):
    message = call.message
    to_exchange_currency = DICT_CURRENCY.get(call.data[-3::])
    currency_list.append(to_exchange_currency)
    msg = bot.send_message(message.chat.id,
                           f'Exchange in {currency_list[0]} to {currency_list[1]}\nSend Amount {currency_list[0]}')
    bot.register_next_step_handler(msg, amount_currency)


def amount_currency(message):
    chat_id = message.chat.id
    try:
        text2 = int(message.text)
    except (ValueError, TypeError):
        bot.send_message(chat_id, 'oops!!!\n\nSend Amount Currency!\nSend Command /exchange')
    else:
        print(type(text2))
        c_list2 = currency_list[0]
        c_list = currency_list[1]
        req = get_user_request(currency_list[0], currency_list[1])
        daily_course = json_api_reader(req)
        course_cur_selected_1 = daily_course.get(c_list)
        course_cur_selected_2 = daily_course.get(c_list2)
        amount = text2 * course_cur_selected_1
        bot.send_message(chat_id,
                         f'Daily Exchange Course💱\n'
                         f'{c_list2} - {course_cur_selected_2}\n'
                         f'{c_list} - {course_cur_selected_1}\n\n'
                         f'<b>Amount</b>{c_list2}: {text2} 💱 {c_list}: {int(amount)}')


if __name__ == '__main__':
    print('Worked! @Exchange_iobot')
    bot.polling()

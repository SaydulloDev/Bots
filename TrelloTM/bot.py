from api_priv import trello_com_bot
from telebot import TeleBot
from utils import write_chat_csv, get_trello_user, get_trello_username_by_chat_id, get_member_task_message
from keyboards import get_inline_boards_btn, get_inline_lists_btn, get_lists_btn, get_members_btn
from trello import TrelloAPIManager
from states import CreateNewTask
import messages

API_TOKEN = trello_com_bot()
bot = TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user = message.from_user.first_name
    bot.send_message(chat_id, messages.start_user_msg(user))


@bot.message_handler(commands=['cancel'])
def cancel(message):
    bot.send_message(message.chat.id, messages.CANCEL)


@bot.message_handler(commands=['auth'])
def auth_handler(message):
    if not get_trello_user("user.csv", message.chat.id):
        bot.send_message(message.chat.id, messages.AUTH)
        bot.register_next_step_handler(message, get_user)
    else:
        bot.send_message(message.chat.id, messages.ALREADY_REG)


def get_user(message):
    write_chat_csv('user.csv', message)
    bot.send_message(message.chat.id, messages.ADDED)


@bot.message_handler(commands=['boards'])
def boards(message):
    if not get_trello_user("user.csv", message.chat.id):
        bot.send_message(message.chat.id, messages.TRELLO_USER_NOT_FOUND)
    else:
        trello_username = get_trello_username_by_chat_id("user.csv", message.chat.id)
        if trello_username:
            bot.send_message(
                message.chat.id, messages.BOARDS,
                reply_markup=get_inline_boards_btn(trello_username, "board_")
            )
        else:
            bot.send_message(message.chat.id, messages.TRELLO_USER_NOT_FOUND)


@bot.callback_query_handler(lambda c: c.data.startswith("board_"))
def get_board_lists(call):
    message = call.message
    trello_username = get_trello_username_by_chat_id("user.csv", message.chat.id)
    trello = TrelloAPIManager(trello_username)
    board_id = call.data.split("_")[2]
    bot.send_message(
        message.chat.id, "Select List:", reply_markup=get_inline_lists_btn(trello, board_id, "show_list_tasks")
    )


@bot.callback_query_handler(lambda c: c.data.startswith("show_list_tasks_"))
def get_member_cards_to_user(call):
    message = call.message
    list_id = call.data.split("_")[3]
    trello_username = get_trello_username_by_chat_id("user.csv", message.chat.id)
    trello = TrelloAPIManager(trello_username)
    card_data = trello.get_cards_on_a_list(list_id)
    msg = get_member_task_message(card_data, trello.get_member_id())
    if msg:
        bot.send_message(message.chat.id, msg)
    else:
        bot.send_message(message.chat.id, messages.NO_TASK)


new_task_user = {}


@bot.message_handler(commands=['new'])
def new_task_user(message):
    if not get_trello_user("user.csv", message.chat.id):
        bot.send_message(message.chat.id, messages.TRELLO_USER_NOT_FOUND)
    else:
        trello_username = get_trello_username_by_chat_id("user.csv", message.chat.id)
        if trello_username:
            bot.send_message(
                message.chat.id, messages.CREATE_TASK,
                reply_markup=get_inline_boards_btn(trello_username, "new_tasks")
            )
        else:
            bot.send_message(message.chat.id, messages.TRELLO_USER_NOT_FOUND)


@bot.callback_query_handler(lambda call: call.data.split('new_tasks_'))
def get_new_task_name(call):
    message = call.message
    trello_username = get_trello_username_by_chat_id("user.csv", message.chat.id)
    trello = TrelloAPIManager(trello_username)
    board_id = call.data.split("_")[2]
    msg = bot.send_message(
        message.chat.id, "Select List:", reply_markup=get_lists_btn(trello, board_id)
    )
    bot.register_next_step_handler(msg, send_new_task_lst)


def send_new_task_lst(message):
    new_task_user['List'] = message.text
    msg = bot.send_message(message.chat.id, messages.TASK_NAME)
    bot.register_next_step_handler(msg, name_task_desc)


def name_task_desc(message):
    new_task_user['Name'] = message.text
    msg = bot.send_message(message.chat.id, messages.TASK_DES)
    bot.register_next_step_handler(msg, select_member)


def select_member(message):
    new_task_user['Description'] = message.text
    msg = bot.send_message(message.chat.id, messages.TASK_MEMBERS)
    bot.register_next_step_handler(msg, selected_member)


def selected_member(message):
    new_task_user['Member'] = message.text
    print(new_task_user)

if __name__ == '__main__':
    try:
        print('Worked!')
        bot.infinity_polling(timeout=1000)
    except KeyboardInterrupt:
        print('Bot Stopped!')

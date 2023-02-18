from api_priv import trello_com_bot
from telebot import TeleBot
from utils import write_chat_csv, get_trello_user, get_trello_username_by_chat_id, get_member_task_message
from keyboards import get_inline_boards_btn, get_inline_lists_btn, get_members_btn
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


@bot.message_handler(commands=["new"])
def create_new_task(message):
    if not get_trello_user("user.csv", message.chat.id):
        bot.send_message(message.chat.id, messages.TRELLO_USER_NOT_FOUND)
    else:
        trello_username = get_trello_username_by_chat_id("user.csv", message.chat.id)
        if trello_username:
            bot.send_message(
                message.chat.id, messages.CREATE_TASK,
                reply_markup=get_inline_boards_btn(trello_username, "new_tasks")
            )
            bot.set_state(message.from_user.id, CreateNewTask.board, message.chat.id)
        else:
            bot.send_message(message.chat.id, messages.TRELLO_USER_NOT_FOUND)


@bot.callback_query_handler(lambda c: c.data.startswith("new_tasks"), state=CreateNewTask.board)
def get_new_task_name(call):
    message = call.message
    trello_username = get_trello_username_by_chat_id("user.csv", message.chat.id)
    trello = TrelloAPIManager(trello_username)
    board_id = call.data.split("_")[2]
    bot.send_message(
        message.chat.id, "Select List:", reply_markup=get_inline_lists_btn(trello, board_id, "list_name")
    )
    bot.set_state(message.from_user.id, CreateNewTask.list, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["task_board_id"] = board_id


@bot.callback_query_handler(lambda c: c.data.startswith("list_name"))
def get_list_id_for_new_task(call):
    message = call.message
    data_ = call.data.split("_")[2]
    msg = bot.send_message(call.from_user.id, messages.TASK_NAME)
    bot.set_state(call.from_user.id, CreateNewTask.name, message.chat.id)
    with bot.retrieve_data(call.from_user.id, message.chat.id) as data:
        data['task_list_id'] = data_
    bot.register_next_step_handler(msg, set_task_name)


def set_task_name(message):
    msg = bot.send_message(message.from_user.id, messages.TASK_DES)
    bot.set_state(message.from_user.id, CreateNewTask.description, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['task_name'] = message.text
        params = {
            'name': data.get('name'),
            'desc': data.get('desc')
        }
    bot.register_next_step_handler(msg, set_task_description)


def set_task_description(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['task_desc'] = message.text
        board_id = data['task_board_id']
    trello_username = get_trello_user('user.csv', message.from_user.id)
    keyboard = get_members_btn(trello_username, board_id, 'new_task_member')
    bot.set_state(message.from_user.id, CreateNewTask.members, message.chat.id)
    bot.send_message(
        message.from_user.id,
        messages.TASK_MEMBERS, reply_markup=keyboard
    )


@bot.callback_query_handler(lambda c: c.data.startswith("new_task_member"))
def get_member_id(call):
    message = call.message
    member_id = call.data.split("_")[3]
    bot.send_message(message.chat.id, messages.LABELS)
    bot.set_state(message.from_user.id, CreateNewTask.members, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["member_id"] = member_id


@bot.callback_query_handler(lambda c: c.data.startswith("create_list_task"))
def get_list_id_for_new_task(call):
    message = call.message
    list_id = call.data.split("_")[3]
    bot.set_state(message.from_user.id, CreateNewTask.name, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as file:
        file["task_list_id"] = list_id


if __name__ == '__main__':
    try:
        print('Worked!')
        bot.polling(timeout=1000)
    except KeyboardInterrupt:
        print('Bot Stopped!')

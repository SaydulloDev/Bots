from telebot import TeleBot, types
from api_priv import translator_io
from text_base import HELP
from request_api import translate

BOT_TOKEN = translator_io()
bot = TeleBot(BOT_TOKEN, parse_mode='html')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    chat_id = message.chat.id
    bot.send_message(chat_id, f'Hello {user.first_name}👋')


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, HELP)


@bot.message_handler(commands=['lang'])
def select_lang(message):
    text_user = message.text
    if 2 <= len(text_user):
        bot.reply_to(message, f'Selected! {text_user} Send Text!')
        return text_user


@bot.message_handler()
def translate_bot(message):
    text_user_t = message.text
    bot.reply_to(message, translate(select_lang(), text_user_t))


if __name__ == '__main__':
    bot.polling()

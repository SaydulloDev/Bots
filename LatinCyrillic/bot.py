from telebot import TeleBot
from api_priv import latin_to_cyrillic
from transliterate import to_latin, to_cyrillic
from msg_bot import start_user

API_TOKEN = latin_to_cyrillic()
bot = TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def welcome_msg(message):
    chat_id = message.chat.id
    user = message.from_user.first_name
    bot.send_message(chat_id, start_user(user))


@bot.message_handler(content_types=['text'])
def convert(message):
    text = message.text
    if text.isascii():
        answer = to_cyrillic(text)
    else:
        answer = to_latin(text)
    bot.reply_to(message, answer)


if __name__ == '__main__':
    print('Worked!')
    bot.polling()

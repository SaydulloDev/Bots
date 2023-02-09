from telebot import TeleBot, types
from command_text import HELP
from api_priv import youtube_io
from pytube_io import send_info

BOT_TOKEN = youtube_io()

bot = TeleBot(BOT_TOKEN, parse_mode='html')


@bot.message_handler(commands=['start'])
def welcome_message(message):
    user = message.from_user
    chat_id = message.chat.id
    bot.send_message(chat_id, f"Hello {user.first_name}👋\n\nWelcome to YouTube Downloader📥\n\nInstruction /help")


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message, HELP)


@bot.message_handler(commands=['download'])
def download(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'SEND ME LINK🔗!')


@bot.message_handler()
def get_link(message):
    chat_id = message.chat.id
    url = message.text
    link = url.find('youtu')
    if 8 <= link:
        yt = send_info(url)
        bot.send_message(chat_id,
                         f"Title >>\n<b>{yt.title}</b>\nAuthor >>\n<b>{yt.author}</b>\nViews >>\n<b>{yt.views}</b>\n"
                         f"Length >>\n<b>{yt.length}</b>")
    else:
        bot.send_message(chat_id, 'SEND LINK!')


if __name__ == "__main__":
    bot.polling()

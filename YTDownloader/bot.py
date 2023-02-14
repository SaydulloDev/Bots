import time

from telebot import TeleBot
from telebot.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton
import os
from command_text import HELP
from api_priv import youtube_io
from pytube_io import download_video480, send_info

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
    button_markup = InlineKeyboardMarkup()
    share = f"https://t.me/share/{url}"
    share_button = InlineKeyboardButton('Share⛓', url=f"{share}")
    link_video = InlineKeyboardButton('Link🔗', url=f'{url}')
    button_markup.add(link_video, share_button)
    if len(url) > 8:
        if url.find('youtu'):
            vid = download_video480(url)
            bot.send_video(chat_id, video=InputFile(vid), caption=f'Format Video 480p',
                           reply_markup=button_markup)
            if os.path.exists(vid):
                time.sleep(100)
                os.remove(vid)
        else:
            bot.send_message(chat_id, 'Send Video Link YouTube!')
    else:
        bot.send_message(chat_id, 'Send Video Link YouTube!')


if __name__ == "__main__":
    print('Worked!')
    bot.polling()

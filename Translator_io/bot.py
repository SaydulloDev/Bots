from telebot import TeleBot
from api_priv import translator_io
from googletrans import LANGUAGES, Translator
from btn_io import inline_button_lang

BOT_TOKEN = translator_io()
bot = TeleBot(BOT_TOKEN, parse_mode='html')


@bot.message_handler(commands=['start'])
def translate_io(message):
    chat_id = message.chat.id
    user = message.from_user
    print(message)
    bot.send_message(chat_id, f"Hello {user.first_name}👋\nI'm Google Translator\nCommand /lang Select Lang")


@bot.message_handler(commands=['lang'])
def select_lang(message):
    bot.send_message(message.chat.id, 'Select Language👇', reply_markup=inline_button_lang)


lang = []


@bot.callback_query_handler(lambda call: call.data.startswith('lang_'))
def send_select_lang(call):
    message = call.message
    lang_user = LANGUAGES.get(call.data[-3::]).title()
    lang.append(lang_user)
    msg = bot.send_message(message.chat.id,
                           f'Translate to {lang_user}\nSend text for translate')
    bot.register_next_step_handler(msg, translate_io_)


def translate_io_(message):
    text_user = message.text
    det_lang = Translator().detect(text_user)
    lang.append(det_lang)
    text_translate = Translator().translate(text_user, dest=lang[0])
    bot.send_message(message.chat.id, text_translate.text)


if __name__ == '__main__':
    bot.polling()

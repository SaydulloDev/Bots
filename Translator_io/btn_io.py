from googletrans import LANGUAGES
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

inline_button_lang = InlineKeyboardMarkup()

for key, value in LANGUAGES.items():
    inline_button_lang.add(InlineKeyboardButton(value, callback_data=f"lang_{key}"))

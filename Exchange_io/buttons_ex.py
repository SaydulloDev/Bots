from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

DICT_CURRENCY = {
    'RUB': 'RUB',
    'AED': 'AED',
    'USD': 'USD',
    'EUR': 'EUR',
    'GBP': 'GBP',
    'UZS': 'UZS',
}
currency_button_inline = InlineKeyboardMarkup()
currency_button_inline2 = InlineKeyboardMarkup()
for key, value in DICT_CURRENCY.items():
    currency_button_inline.add(
        InlineKeyboardButton(key, callback_data=f"currency_{value}")
    )
    currency_button_inline2.add(
        InlineKeyboardButton(key, callback_data=f"to_currency_{value}")
    )

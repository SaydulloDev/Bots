# Telegram Exchange Bot

API for Rapid API
- [ExchangeRatesPro](https://rapidapi.com/ExchangeRatesPro/api/exchangeratespro/)

Package
- PyTelegramBotAPI

Files About
- bot.py [main]
- api_request.py [request api]
- json.read.py [json reader]
- buttons_ex.py [buttons file]
- msg_bot/py [messages bot command]

## Code About
### /start
```python
@bot.message_handler(commands=['start'])
def welcome_msg(message):
    chat_id = message.chat.id
    user = message.from_user
    bot.send_message(chat_id, start_user_msg(user.first_name))
```

Result Photo👇

![](https://www.linkpicture.com/q/1_812.png)

### /exchange
Step 1 Select 
```python
@bot.message_handler(commands=['exchange'])
def exchange_currency(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Select Currency👇', reply_markup=currency_button_inline)
```

Result Photo👇

![](https://www.linkpicture.com/q/2_932.png)

Step 2 Converting

```python
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

```

Result Photo👇

![](https://www.linkpicture.com/q/3_379.png)
# Translator Bot

Packages 
- Googletrans
- PyTelegram

Files
- bot [main]
- btn_io.py [buttons]

Code About
## /start
```python
@bot.message_handler(commands=['start'])
def translate_io(message):
    chat_id = message.chat.id
    user = message.from_user
    print(message)
    bot.send_message(chat_id, f"Hello {user.first_name}👋\nI'm Google Translator\nCommand /lang Select Lang")
```

This handler is responsible for the /start command

![](https://www.linkpicture.com/q/Screenshot-from-2023-02-14-20-51-55.png)

## /lang
```python
@bot.message_handler(commands=['lang'])
def select_lang(message):
    bot.send_message(message.chat.id, 'Select Language👇', reply_markup=inline_button_lang)
```
When sending the /lang command. the user can choose the language to translate

![](https://www.linkpicture.com/q/Screenshot-from-2023-02-14-20-53-39.png)

## message for translate

![](https://www.linkpicture.com/q/Screenshot-from-2023-02-14-20-53-51.png)

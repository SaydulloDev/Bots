# Latin to Cyrillic Telegram Bot

Files
- bot.py [main]
- transliterate.py [main 2lvl]
- msg_bot.py [messages]

Codes About
```python
@bot.message_handler(content_types=['text'])
def convert(message):
    text = message.text
    if text.isascii():
        answer = to_cyrillic(text)
    else:
        answer = to_latin(text)
    bot.reply_to(message, answer)

```
This is Message Handler only Text type message

![](https://www.linkpicture.com/q/rr_1.png)
This is Answer Bot

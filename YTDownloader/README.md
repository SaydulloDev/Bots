# YouTube Video Downloader

Telegram bot >> [@YouTube_ioBot](https://t.me/YouTube_ioBot)

Packages

- PyTube
- PyTelegramBotAPI

Python Files

- bot.py [main file]
- pytube_io [Pytube Package File]
- command_text.py [Text Messages]

## Code About

- bot.py

```python
@bot.message_handler()
def get_link(message):
    chat_id = message.chat.id
    url = message.text
    button_markup = InlineKeyboardMarkup()
    share = f"https://t.me/share/{url}"
    share_button = InlineKeyboardButton('Share⛓', url=f"{share}")
    link_video = InlineKeyboardButton('Link🔗', url=f'{url}')
    button_markup.add(link_video, share_button)
    if url.find('youtu'):
        vid = download_video480(url)
        bot.send_video(chat_id, video=InputFile(vid), caption=f'Format Video 480p',
                       reply_markup=button_markup)
        if os.path.exists(vid):
            time.sleep(10)
            os.remove(vid)
    else:
        bot.send_message(chat_id, 'Send Video Link YouTube!')
```

This Message Handler is Responsible for the Link of the YouTube Video and sends the video user chat.

![](https://www.linkpicture.com/q/Screenshot-from-2023-02-14-16-00-28.png)

If The User Sends the wrong Link then reply like this
- Send Video Link YouTube

![](https://www.linkpicture.com/q/Screenshot-from-2023-02-14-16-00-47.png)

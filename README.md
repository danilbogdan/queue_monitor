Telegram bot that helps to catch free slot in the Queue

1. Install requirements
2. Specify parameters in settings.py
```
PHONE_FIRST = '' # your phone number
QUEUE_SITE = ''  # your queue url (site where to monitor queue)
TWO_CAPTCHA_API_KEY = ''  # your 2captcha API KEY
TG_APIKEY = ''  # your telegram bot api key
CHAT_ID =   # your telegram chat id where to send notifications
```
3. Run both tgbot.py
4. Send /start to your bot and you will see your `CHAT_ID`
5. Copy it to your settings.py
6. Run main.py

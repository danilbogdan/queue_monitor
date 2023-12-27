import io
import json
import requests
import time
from PIL import Image
from base64 import b64encode, b64decode
from datetime import datetime
from twocaptcha import TwoCaptcha

import api
import settings
from parser import parse_date
from tgbot import bot, clear_keyboard

url = settings.QUEUE_SITE

solver = TwoCaptcha(TWO_CAPTCHA_API_KEY)

PHPSESSID = api.get_session_id()
headers = api.get_headers()


class QueueRegistrator:
    def __init__(self):
        self.session = requests.Session()

    def resolve_captcha(self):
        task = self.session.get('https://captcha.cherg.net/v3/challenge')
        task_data = task.json()
        challenge = task_data['challenge']
        img_base64 = task_data['image'].split(',')[-1]
        img = Image.open(io.BytesIO(b64decode(img_base64)))
        img = img.resize((500, 380))
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_base64 = b64encode(buffered.getvalue()).decode('utf-8')
        hints = {"hints": task_data['solve']['selectHints']}
        result = solver.normal(img_base64, lang='uk', numeric=1, hintText=json.dumps(hints))
        response = self.session.post('https://captcha.cherg.net/v3/solve',
                                     json={"challenge": challenge, "solve": result['code']})
        print(response.json()['solve'])
        return response.json()['captcha']

    def make_get(self, route):
        response = self.session.get(f'{url}?route={route}&PHPSESSID={PHPSESSID}', headers=headers)
        time.sleep(1)
        return response

    def make_post(self, route, data):
        response = self.session.post(f'{url}?route={route}', data=data, headers=headers)
        time.sleep(1)
        return response


# Press the green button in the gutter to run the script.
def check_queue():
    s = QueueRegistrator()
    s.make_get(api.PHONE)
    s.make_post(api.SELECT_PHONE, {
        'country-code': settings.COUNTRY_CODE_PL,
        'PHPSESSID': PHPSESSID,
        'phone-first': settings.PHONE_FIRST,
        'sign': '',
        'expire': ''
    })
    s.make_post(api.REGION, {
        'PHPSESSID': PHPSESSID,
    })
    resp = s.make_post(api.REGION_SELECT, {
        'PHPSESSID': PHPSESSID,
        'region[id]': '780',
        'region[name]': 'ВРОЦЛАВ',
        'org[id]': '0',
        'org[name]': 'Оберіть підрозділ',
        'org[address]': '',
    })
    resp = s.make_post(api.ORGANIZATION, {
        'PHPSESSID': PHPSESSID,
        'region[id]': '780',
        'region[name]': 'ВРОЦЛАВ',
    })
    resp = s.make_post(api.SERVICE, {
        'PHPSESSID': PHPSESSID,
        'region[id]': '780',
        'region[name]': 'ВРОЦЛАВ',
        'org[id]': '2042',
        'org[name]': 'Паспортний сервіс в м.Вроцлав',
        'org[address]': 'plac Grunwaldzki 22, 50-363 Wrocław'
    })

    captch = s.resolve_captcha()

    s.make_post(api.SERVICE_SELECT, {
        'PHPSESSID': PHPSESSID,
        'captcha': captch,
        'service[id]': settings.SERVICE_ID,
        'service[global_id]': '1',
        'service[name]': 'Оформлення документів',
        'service[type]': 'type_passport',

    })
    resp = s.make_post(api.DATELINE, {
        'PHPSESSID': PHPSESSID,
    })
    print(resp.content)
    return parse_date(resp.content)


if __name__ == '__main__':
    CHECK_EVERY_N_MIN = 1
    CHECK_FIRST_N_MIN = 16
    while True:
        now = datetime.now()
        if now.minute < CHECK_FIRST_N_MIN and 3 < now.hour < 13:
            try:
                print('start checking queue')
                available_date = check_queue()
                if not available_date:
                    raise Exception('No date available for today')
                bot.send_message(CHAT_ID,
                                 text='Hello. I will help you to catch up slot in the queue!',
                                 reply_markup=clear_keyboard())
            except Exception as e:
                bot.send_message(CHAT_ID,
                                 text=f"Can't get place in queue: {str(e)}",
                                 reply_markup=clear_keyboard())

            bot.send_message(CHAT_ID,
                             text=f"Sleep for {CHECK_EVERY_N_MIN} until the next attempt...",
                             reply_markup=clear_keyboard())
        else:
            print('skip: not in time')
        time.sleep(CHECK_EVERY_N_MIN * 60)

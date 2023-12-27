import telebot

import settings

bot = telebot.TeleBot(settings.TG_APIKEY)
bot.add_custom_filter(telebot.custom_filters.TextContainsFilter())


def CheckQueueButton():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = telebot.types.KeyboardButton(text="Check queue")
    keyboard.add(button_geo)
    return keyboard


def clear_keyboard():
    return telebot.types.ReplyKeyboardRemove()


@bot.message_handler(commands=['start'])
def start_handler(message: telebot.types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     text=f'Hello. I will help you to catch up free slots in the queue! Your chat id is: {chat_id}',
                     reply_markup=CheckQueueButton())


if __name__ == '__main__':
    bot.infinity_polling()

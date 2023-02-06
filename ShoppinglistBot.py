import os
import telegram

def main(chat_id):
    bot = telegram.Bot(token=os.environ['TELEGRAM_API_TOKEN'])
    bot.send_message(chat_id=chat_id, text='Hello, world!')
    return 'Message sent!'

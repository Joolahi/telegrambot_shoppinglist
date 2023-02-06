
import sqlite3
import os
from flask import Flask, request
from telegram.bot import Bot

TOKEN = '5945945191:AAEG4NkyYNSSmHXHO_mqTiQLZnqAopGnQDo'
bot = Bot(token=TOKEN)

def start(chat_id):
    bot.send_message(chat_id=chat_id,text='Shopping list, \n /add -> add item to shopping list \n /show -> will show you what is on the list')


def adding(chat_id, items):
    database = sqlite3.connect('Shoppinglist.db')
    connect = database.cursor()
    connect.execute("CREATE TABLE IF NOT EXISTS shopping_list (id INTEGER PRIMARY KEY, item TEXT)")
    for item in items:
        connect.execute("INSERT INTO shopping_list (item) VALUES (?)", (item,))
    database.commit()
    database.close()
    bot.send_message(chat_id=chat_id, text="Item addded to shopping list!")




def showingList(chat_id):
    database = sqlite3.connect('Shoppinglist.db')
    connect = database.cursor()
    connect.execute("SELECT item FROM shopping_list")
    items = [item[0] for item in connect.fetchall()]
    database.close
    if not items:
        bot.send_message(chat_id=chat_id, text="Shopping list is empty.")
    else:
        bot.send_message(chat_id=chat_id, text="Shopping list:\n\n" + "\n".join(items))

server = Flask(__name__)

def getMessage():
    update = request.get_json(force=True)
    chat_id = update["message"]["chat"]["id"]
    text = update["message"]["text"]
    if text == "/start":
        start(chat_id)
    elif text.startswith("/add"):
        items = text.split()[1:]
        adding(chat_id, items)
    elif text == "/list":
        showingList(chat_id)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))

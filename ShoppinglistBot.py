from telegram.ext import Updater, CommandHandler
import sqlite3
import os
from flask import Flask, request

TOKEN = '5945945191:AAEG4NkyYNSSmHXHO_mqTiQLZnqAopGnQDo'

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    update.message.reply_text('Shopping list, \n /add -> add item to shopping list \n /show -> will show you what is on the list')


def adding(update, context):
    args = context.args
    database = sqlite3.connect('Shoppinglist.db')
    connect = database.cursor()
    connect.execute("CREATE TABLE IF NOT EXISTS shopping_list (id INTEGER PRIMARY KEY, item TEXT)")
    for item in args:
        connect.execute("INSERT INTO shopping_list (item) VALUES (?)", (item,))
    database.commit()
    database.close()
    update.message.reply_text("Item addded to shopping list!")




def showingList(update, context):
    database = sqlite3.connect('Shoppinglist.db')
    connect = database.cursor()
    connect.execute("SELECT item FROM shopping_list")
    items = [item[0] for item in connect.fetchall()]
    database.close
    if not items:
        update.message.reply_text('Shopping list is empty')
    else:
        update.message.reply_text('Shopping list: \n' + '\n'.join(items))

DA = dispatcher.add_handler
start_handler = CommandHandler('start',start)
DA(start_handler)
add_handler = CommandHandler('add',adding)
DA(add_handler)
list_handler = CommandHandler('show',showingList)
DA(list_handler)

server = Flask(__name__)

def getMessage():
    updater.dispatcher(request.get_json(force=True))
    return '!', 200

if __name__ == "__main__":
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

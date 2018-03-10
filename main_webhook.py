'''
A. Simonov 2018
Entry point to app
MIT
'''
# Std Eggs
import threading
import time
# Third-pathy modules
from flask import Flask, request
import telebot
# Local modules
from modules.watcher import watchdoge
from modules.torrent import Torrent
from modules.action_handlers import text_parser, callback_handler, get_torr_file
from interface.keyboards import server_kbd, torr_kbd
import interface.strings as cs
import config as cfg

# Consts
bot = telebot.TeleBot(cfg.TOKEN)
tr = Torrent()
# Keyboards
torr_kbd(bot)
server_kbd(bot)


class Watcher(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            # print('===================================================')
            # print(f'[x] {datetime.datetime.now()}::Watcher - Starting ')
            watchdoge(bot, tr)
            # print(f'[x] {datetime.datetime.now()}::Watcher - Stopping ')
            # print('===================================================')
            time.sleep(60)
        # print(f'[x] {datetime.datetime.now()}::Watcher - Stopped ')


# Apps
app = Flask(__name__)
watch = Watcher(1, 'Thread-1', 1)


# Webhook
@app.route(f'/api/tg/{cfg.TOKEN}/', methods=['GET', 'POST'])
def get_updates():
    if request.method == 'POST':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        text = ''
        for i in request.headers:
            text += '=='.join(i) + '\n'
        return '<pre>' + text + '</pre>'


# Handle all from Telegram =================================
@bot.message_handler(commands=['help'])
def send_welcome(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'upload_document')
    bot.send_message(chat_id, cs.helpText, parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def txt_queries(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'upload_document')
    text_parser(tr, bot, message)
    return 'OK'


@bot.message_handler(content_types=['document'])
def torr_file(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'upload_document')
    get_torr_file(tr, bot, message)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    bot.send_chat_action(chat_id, 'upload_document')
    callback_handler(tr, bot, call)
    return 'OK'
# End Handle all from Telegram =================================


if __name__ == "__main__":
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=cfg.WEBHOOK_URL_BASE + cfg.WEBHOOK_URL_PATH)
    watch.start()
    time.sleep(20)
    app.run(port=4003, host='0.0.0.0', debug=True, use_reloader=True)

    print('\nSome App Stoped!')

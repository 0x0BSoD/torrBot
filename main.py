# _*_ coding: utf-8 _*_
import telebot
import time

from utils.logger import log
from utils.router import parse
import interface.strings as cs
from interface.keyboards import server_kbd, torr_kbd
import config as cfg

bot = telebot.TeleBot(cfg.token)
print(bot.get_me())
errVideo = open('./media/error.mp4', 'rb')

# Keyboards
torr_kbd(bot)
server_kbd(bot)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    log(message, cs.helpText)
    bot.reply_to(message, cs.helpText)


@bot.message_handler(content_types=['text'])
def echo_all(message):
    bot.send_chat_action(message.chat.id, 'upload_document')
    reply = parse(message.text)
    if not reply['status']:
        log(message, 'Error!')
        bot.send_message(message.chat.id, reply['message'])
        bot.send_video(message.chat.id, errVideo)
    else:
        log(message, reply)
        bot.send_message(message.chat.id, reply['message'], parse_mode="html")


@bot.message_handler(content_types=['document'])
def echo_all(message):
    name = message.document.file_name
    try:
        ext = name.split(".")[1]
        if ext == 'torrent':
            log(message, 'Get File!')
            f_id = message.document.file_id
            file_info = bot.get_file(f_id)
            downloaded_file = bot.download_file(file_info.file_path)
            path = f'{cfg.torrentsDir}/{f_id}.torrent'
            with open(path, 'wb') as new_file:
                new_file.write(downloaded_file)
            log(message, 'Added!')
            bot.send_message(message.chat.id, f'{name} == Added!')
        else:
            log(message, 'Error!')
            bot.send_message(message.chat.id, 'It\'s not torrent file!')
            bot.send_video(message.chat.id, errVideo)
    except Exception as e:
            log(message, 'Error!')
            bot.send_message(message.chat.id,
                             'Some Error ( ⚆ _ ⚆ ) {}'.format(e),
                             parse_mode="html")
            bot.send_video(message.chat.id, errVideo)


def main_loop():
    bot.polling(True)
    while 1:
        time.sleep(3)


if __name__ == '__main__':
    main_loop()
    errVideo.close()

# _*_ coding: utf-8 _*_
import telebot
import json
import requests

from pathlib import Path
from modules.logger import log
from modules.router import parse
from modules import strings as cs
import config as cfg

bot = telebot.TeleBot(cfg.token)
print(bot.get_me())

errVideo = open('./media/error.mp4', 'rb')


@bot.message_handler(commands=['start', 'back'])
def handle_start(message):
    userMarkup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                   one_time_keyboard=False)
    userMarkup.row('/torrent_сontrols')
    userMarkup.row('chmod 777', 'Dir Content')
    userMarkup.row('CPU', 'Free Space')
    bot.send_message(message.from_user.id,
                     cs.helloText,
                     reply_markup=userMarkup)


@bot.message_handler(commands=['torrent_сontrols'])
def handle_start(message):
    userMarkup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                   one_time_keyboard=False)
    userMarkup.row('Start All', 'Stop All')
    userMarkup.row('Activity', 'Ratio')
    userMarkup.row('/back')
    bot.send_message(message.from_user.id,
                     cs.helloText,
                     reply_markup=userMarkup)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    log(message, cs.helpText)
    bot.reply_to(message, cs.helpText)


@bot.message_handler(content_types=['text'])
def echo_all(message):
    bot.send_chat_action(message.chat.id, 'upload_document')
    reply = parse(message.text)
    if not reply['status']:
        log(message, 'Errored!')
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
            path = '{}/{}.torrent'.format(cfg.torrentsDir, f_id)
            with open(path, 'wb') as new_file:
                new_file.write(downloaded_file)
            log(message, 'Added!')
            bot.send_message(message.chat.id, "<b>{} Added!</b>".format, parse_mode="html")
        else:
            log(message, 'Errored!')
            bot.send_message(message.chat.id, 'It\'s not torrent file!')
            bot.send_video(message.chat.id, errVideo)
    except Exception as e:
            log(message, 'Errored!')
            bot.send_message(message.chat.id, 'Some Fucking Error ( ⚆ _ ⚆ )')
            bot.send_video(message.chat.id, errVideo)


bot.polling(none_stop=True, interval=0)
errVideo.close()

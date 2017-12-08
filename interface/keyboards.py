import telebot
from utils import strings as cs


class kbd:
    def serverKbd(bot):
        @bot.message_handler(commands=['start', 'back'])
        def handle_start(message):
            um = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                   one_time_keyboard=False)
            um.row('/torrent_сontrols')
            um.row('chmod 777', 'Dir Content')
            um.row('CPU', 'Free Space')
            bot.send_message(message.from_user.id,
                             cs.helloText,
                             reply_markup=um)

    def torrKbd(bot):
        @bot.message_handler(commands=['torrent_сontrols'])
        def handle_start(message):
            um = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                                   one_time_keyboard=False)
            um.row('Start All', 'Stop All')
            um.row('Activity', 'Ratio')
            um.row('/back')
            bot.send_message(message.from_user.id,
                             cs.helloText,
                             reply_markup=um)

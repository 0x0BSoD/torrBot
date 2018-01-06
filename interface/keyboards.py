import telebot
import interface.strings as cs


def server_kbd(bot):
    @bot.message_handler(commands=['start', 'back'])
    def handle_start(message):
        um = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                               one_time_keyboard=False)
        um.row('/torrent_control')
        um.row('chmod 777', 'Dir Content')
        um.row('CPU', 'Free Space')
        bot.send_message(message.from_user.id,
                         cs.helloText,
                         reply_markup=um)


def torr_kbd(bot):
    @bot.message_handler(commands=['torrent_control'])
    def handle_start(message):
        um = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
                                               one_time_keyboard=False)
        um.row('Start All', 'Stop All')
        um.row('Get Status', 'Torrents')
        um.row('/back')
        bot.send_message(message.from_user.id,
                         cs.helloText,
                         reply_markup=um)

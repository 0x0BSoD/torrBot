from telebot import types
import interface.strings as cs


def server_kbd(bot):
    @bot.message_handler(commands=['start', 'back'])
    def handle_start(message):
        um = types.ReplyKeyboardMarkup(resize_keyboard=True,
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
        um = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                               one_time_keyboard=False)
        um.row('Start All', 'Stop All')
        um.row('Get Status', 'Torrents')
        um.row('/back')
        bot.send_message(message.from_user.id,
                         cs.helloText,
                         reply_markup=um)


def inline_kbd(torr_id, status):
    """Return the inlaine keyboard based on status.

    Keyword arguments:
    torr_id -- integer
    status -- integer
    """
    keyboard = types.InlineKeyboardMarkup()

    start_button = types.InlineKeyboardButton(text="Start", callback_data=f'start_{torr_id}')
    stop_button = types.InlineKeyboardButton(text="Stop", callback_data=f'stop_{torr_id}')
    remove_button = types.InlineKeyboardButton(text="Remove", callback_data=f'delete_{torr_id}')
    if status == 'stated':
        keyboard.add(stop_button, remove_button)
    else:
        keyboard.add(start_button, remove_button)
    return keyboard
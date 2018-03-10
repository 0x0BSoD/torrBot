from telebot import types
import interface.strings as cs


def server_kbd(bot):
    @bot.message_handler(commands=['start', 'back'])
    def handle_start(message):
        um = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                               one_time_keyboard=False)
        um.row('/torrent_control')
        um.row('CPU', 'Free Space', 'Dir Content')
        bot.send_message(message.from_user.id,
                         cs.helloText,
                         reply_markup=um)


def torr_kbd(bot):
    @bot.message_handler(commands=['torrent_control'])
    def handle_start(message):
        um = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                               one_time_keyboard=False)
        um.row('Get Status', 'Torrents')
        um.row('/back')
        bot.send_message(message.from_user.id,
                         cs.helloText,
                         reply_markup=um)


def torr_inline_kbd(torr_id, status, kb_type):
    """Return the inline keyboard based on status.

    Keyword arguments:
    torr_id -- integer
    status -- integer
    """
    keyboard = types.InlineKeyboardMarkup()

    start_button = types.InlineKeyboardButton(text="Start", callback_data=f'start_{torr_id}')
    stop_button = types.InlineKeyboardButton(text="Stop", callback_data=f'stop_{torr_id}')
    if kb_type == 'short':
        info_button = types.InlineKeyboardButton(text="🔻 More", callback_data=f'info_{torr_id}')
    else:
        info_button = types.InlineKeyboardButton(text="🔺 Less", callback_data=f'back_{torr_id}')
    remove_button = types.InlineKeyboardButton(text="Remove", callback_data=f'delete_{torr_id}')
    if status == 'started':
        keyboard.add(info_button, stop_button, remove_button)
    else:
        keyboard.add(info_button, start_button, remove_button)
    return keyboard


def remove_torr_kbd(torr_id):
    keyboard = types.InlineKeyboardMarkup()

    yes_button = types.InlineKeyboardButton(text="Yes", callback_data=f'delyes_{torr_id}')
    no_button = types.InlineKeyboardButton(text="No", callback_data=f'back_{torr_id}')

    keyboard.add(yes_button, no_button)
    return keyboard


def status_inline_kbd():
    """Return the inline keyboard based on status.

    Keyword arguments:
    torr_id -- integer
    status -- integer
    """
    keyboard = types.InlineKeyboardMarkup()

    start_button = types.InlineKeyboardButton(text="Start All", callback_data='start_all')
    stop_button = types.InlineKeyboardButton(text="Stop All", callback_data='stop_all')
    keyboard.add(start_button, stop_button)
    return keyboard

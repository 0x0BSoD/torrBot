from modules.router import parse, parse_callback
import config as cfg


def text_parser(tr, bot, message):
    reply = parse(tr, message.text)
    try:
        for i in reply:
            if not i['status']:
                bot.send_message(message.chat.id, i['message'])
                err_video = open('media/error.mp4', 'rb')
                bot.send_video(message.chat.id, err_video)
                err_video.close()
            else:
                if i['keyboard']:
                    bot.send_message(message.chat.id,
                                     i['message'],
                                     parse_mode="html",
                                     reply_markup=i['keyboard'])
                else:
                    bot.send_message(message.chat.id,
                                     i['message'],
                                     parse_mode="html")
    except TypeError:
        if not reply['status']:
            bot.send_message(message.chat.id, reply['message'])
            err_video = open('media/error.mp4', 'rb')
            bot.send_video(message.chat.id, err_video)
            err_video.close()
        else:
            if reply['keyboard']:
                bot.send_message(message.chat.id,
                                 reply['message'],
                                 parse_mode="html",
                                 reply_markup=reply['keyboard'])
            else:
                bot.send_message(message.chat.id,
                                 reply['message'],
                                 parse_mode="html")


def callback_handler(tr, bot, call):
    if call.message:
        reply = parse_callback(tr, call.data)
        try:
            for i in reply:
                if not i['status']:
                    err_video = open('media/error.mp4', 'rb')
                    bot.send_message(call.message.chat.id, i['message'])
                    bot.send_video(call.message.chat.id, err_video)
                    err_video.close()
                else:
                    if i['edit']:
                        if i['keyboard']:
                            bot.edit_message_text(i['message'],
                                                  chat_id=call.message.chat.id,
                                                  message_id=call.message.message_id,
                                                  parse_mode="html",
                                                  reply_markup=i['keyboard'])
                        else:
                            bot.edit_message_text(call.message.chat.id,
                                                  call.message.message_id,
                                                  i['message'],
                                                  parse_mode="html")
                    else:
                        if i['keyboard']:
                            bot.send_message(call.message.chat.id,
                                             i['message'],
                                             parse_mode="html",
                                             reply_markup=i['keyboard'])
                        else:
                            bot.send_message(call.message.chat.id,
                                             i['message'],
                                             parse_mode="html")
        except TypeError:
            err_video = open('media/error.mp4', 'rb')
            bot.send_message(call.message.chat.id, reply['message'])
            bot.send_video(call.message.chat.id, err_video)
            err_video.close()


def get_torr_file(tr, bot, message):
    name = message.document.file_name
    try:
        ext = name.split(".")[1]
        if ext == 'torrent':
            f_id = message.document.file_id
            file_info = bot.get_file(f_id)
            downloaded_file = bot.download_file(file_info.file_path)
            path = f'{cfg.torrentsDir}/{f_id}.torrent'
            with open(path, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.send_message(message.chat.id, f'{name} == Added!')
        else:
            bot.send_message(message.chat.id, 'It\'s not torrent file!')
            err_video = open('media/error.mp4', 'rb')
            bot.send_video(message.chat.id, err_video)
            err_video.close()
    except Exception as e:
        bot.send_message(message.chat.id,
                         'Some Error ( ⚆ _ ⚆ ) {}'.format(e),
                         parse_mode="html")
        err_video = open('media/error.mp4', 'rb')
        bot.send_video(message.chat.id, err_video)
        err_video.close()
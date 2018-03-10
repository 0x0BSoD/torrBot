''' only watchdoge! '''
import datetime
from json import dumps

from modules.sqll_wrapper import get_by_torr_id, insert_to_bd, update_state
from interface.strings import ready_text
import config as cfg

# https://api.telegram.org/bot432397698:AAE6GlNcchU7gsjCPJVbjkxCiVd_bJKiNKU/getUpdates


def get_one(data):
    return data['data'][0]


def watchdoge(bot, tr):
    ''' watchdoge(void) -> bool
    
    Get Active Torrents and check state.
    If done, send message and set send flag in base '''
    # try:
    response = tr.get_all()

    if response['result'] == 'success':
        for i in response['data']:
            in_base = get_by_torr_id(i['id'])
            if in_base:
                if i['percentDone'] == 1 and in_base[6] != 1:
                    name = get_one(tr.get_by_id(i['id']))
                    bot.send_message(chat_id=cfg.tg_chat, text=ready_text.format(name["name"]))
                    update_state(i['id'])
            else:
                data = (i['id'], i['name'], dumps(i), 0, 0, datetime.datetime.now())
                insert_to_bd(data)
        return True
    else:
        pass
    # except Exception as e:
    #     print(f'[x] {datetime.datetime.now()}::Watcher - crashed x_x ')
    #     print(f'Host {e} not found or down...')
    #     return False
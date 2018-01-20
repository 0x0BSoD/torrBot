import utils.torrent as torr
from utils.dir_utils import get_folder_items, fix_rights
from utils.server_status import sys_health, disc_free


def parse_id(data):
    try:
        torr_id = data.split('_')[1]
        return torr_id
    except IndexError:
        return False


def parse(message):
    try:
        if message.startswith('magnet'):
            return torr.add_by_magnetlink(message)
        elif message.startswith('Get Status'):
            return torr.get_status()
        elif message.startswith('CPU'):
            return sys_health()
        elif message.startswith('Free Space'):
            return disc_free()
        elif message.startswith('chmod 777'):
            return fix_rights()
        elif message.startswith('Dir Content'):
            return get_folder_items()
        elif message.startswith('Start All'):
            return torr.start_all()
        elif message.startswith('Stop All'):
            return torr.stop_all()
        elif message.startswith('Torrents'):
            return torr.get_all_torrents()
        elif 'Info_' in message:
            torr_id = parse_id(message)
            if torr_id:
                return torr.torrent_info(torr_id)
            else:
                raise ValueError('Error on getting info.')
        elif 'Stop_' in message:
            torr_id = parse_id(message)
            if torr_id:
                return torr.stop_by_id(torr_id)
            else:
                raise ValueError('Error on stopping torrent.')
        elif 'Start_' in message:
            torr_id = parse_id(message)
            if torr_id:
                return torr.start_by_id(torr_id)
            else:
                raise ValueError('Error on starting torrent.')
        elif 'Delete_' in message:
            torr_id = parse_id(message)
            if torr_id:
                return torr.delete_by_id(torr_id)
            else:
                raise ValueError('Error on deleting torrent.')
        else:
            return {'status': True,
                    'message': 'Don\'t get it (~ ~)'}
    except ValueError as err:
        return {'status': True,
                'message': f'Error in Query:{err}'}


def parse_callback(data):
    if 'stop_' in data:
        torr_id = data.split('_')[1]
        return torr.stop_by_id(torr_id)
    elif 'start_' in data:
        torr_id = data.split('_')[1]
        return torr.start_by_id(torr_id)
    elif 'delete_' in data:
        torr_id = data.split('_')[1]
        return torr.delete_by_id(torr_id)

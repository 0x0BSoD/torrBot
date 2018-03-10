from modules.dir_utils import get_folder_items, fix_rights
from modules.server_status import sys_health, disc_free


def parse_id(data):
    try:
        torr_id = data.split('_')[1]
        return torr_id
    except IndexError:
        return False


def parse(torr, message):
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
        # elif 'Info_' in message:
        #     torr_id = parse_id(message)
        #     if torr_id:
        #         return torr.torrent_info(torr_id)
        #     else:
        #         raise ValueError('Error on getting info.')
        # elif 'Stop_' in message:
        #     torr_id = parse_id(message)
        #     if torr_id:
        #         return torr.stop_by_id(torr_id)
        #     else:
        #         raise ValueError('Error on stopping torrent.')
        # elif 'Start_' in message:
        #     torr_id = parse_id(message)
        #     if torr_id:
        #         return torr.start_by_id(torr_id)
        #     else:
        #         raise ValueError('Error on starting torrent.')
        # elif 'Delete_' in message:
        #     torr_id = parse_id(message)
        #     if torr_id:
        #         return torr.delete_by_id(torr_id)
        #     else:
        #         raise ValueError('Error on deleting torrent.')
        else:
            return {'status': True,
                    'message': 'Don\'t get it (~ ~)',
                    'keyboard': False}
    except ValueError as err:
        return {'status': True,
                'message': f'Error in Query:{err}',
                'keyboard': False}


def parse_callback(torr, data):
    try:
        if '_' in data and 'all' not in data:
            torr_id = int(data.split('_')[1])
        else:
            torr_id = ''
        if data == 'start_all':
            return torr.start_all()
        elif data == 'stop_all':
            return torr.stop_all()
        elif 'info_' in data:
            return torr.torrent_info(torr_id)
        elif 'stop_' in data:
            return torr.stop_by_id(torr_id)
        elif 'start_' in data:
            return torr.start_by_id(torr_id)
        elif 'delete_' in data:
            return torr.delete_by_id(torr_id)
        elif 'delyes_' in data:
            return torr.delete_by_id_confirm(torr_id)
        elif 'back_' in data:
            return torr.get_short(torr_id)
        else:
            return {'status': False,
                    'message': f'No action for:{data}',
                    'keyboard': False}
    except AttributeError as err:
        return {'status': False,
                'message': f'Error in Callback:{err}',
                'keyboard': False}

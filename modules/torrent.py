"""
Module for control transmission daemon through rpc
"""
# import sys
import os
import math
import time
from datetime import datetime
from urllib.parse import unquote
from json import loads, dumps
from requests import get, post

from interface.keyboards import status_inline_kbd, torr_inline_kbd, remove_torr_kbd
import interface.strings as cs
import config as cfg

EPOCH = datetime.utcfromtimestamp(0)


class Torrent:
    """ Torrents actions """
    session_id = None
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Torrent, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        ping_url = cfg.url.split('/')[2].split(':')[0]
        response = os.system(f'ping -c 1 {ping_url} > /dev/null')
        if response != 0:
            raise Exception(ping_url) 
        sessionid_request = get(cfg.url,
                                auth=(cfg.username, cfg.password),
                                verify=cfg.verify)
        self.session_id = sessionid_request.headers['x-transmission-session-id']
    
    def __repr__(self):
        return f'Transmission ID: {self.session_id}\nDaemon URL: {cfg.url}'
    
    def __str__(self):
        return self.session_id

    def timestamp_to_datetime(self, timestamp, epoch=EPOCH):
        ''' Get time stamp amd return date '''
        epoch = datetime.fromordinal(epoch.toordinal())
        epoch_difference = self.timedelta_to_seconds(epoch - EPOCH)
        adjusted_timestamp = timestamp - epoch_difference
        date = datetime.fromtimestamp(adjusted_timestamp)
        return str(date)

    @staticmethod
    def take_state(data, kb_type):
        if not data['errorString']:
            if data['status'] == 0:
                icon = '⏹️️'
                status = 'Torrent is stopped'
                menu = torr_inline_kbd(data['id'], 'stopped', kb_type)
            elif data['status'] == 1:
                icon = '▶️'
                status = 'Queued to check files'
                menu = torr_inline_kbd(data['id'], 'started', kb_type)
            elif data['status'] == 2:
                icon = '▶️'
                status = 'Checking files'
                menu = torr_inline_kbd(data['id'], 'started', kb_type)
            elif data['status'] == 3:
                icon = '▶️'
                status = 'Queued to download'
                menu = torr_inline_kbd(data['id'], 'started', kb_type)
            elif data['status'] == 4:
                icon = '▶️'
                status = 'Downloading'
                menu = torr_inline_kbd(data['id'], 'started', kb_type)
            elif data['status'] == 5:
                icon = '▶️'
                status = 'Queued to seed'
                menu = torr_inline_kbd(data['id'], 'started', kb_type)
            else:
                icon = '▶️'
                status = 'Seeding'
                menu = torr_inline_kbd(data['id'], 'started', kb_type)
        else:
            icon = '🔥️'
            status = data['errorString']
            menu = torr_inline_kbd(data['id'], 'stopped', kb_type)
        return icon, status, menu

    @staticmethod
    def timedelta_to_seconds(delta):
        ''' Get delta and return his in seconds '''
        seconds = (delta.microseconds * 1e6) + delta.seconds + (delta.days * 86400)
        seconds = abs(seconds)
        return seconds

    @staticmethod
    def convert_sizes(size_bytes, units='s'):
        """ Covert units:
        units 's' - storage, 'n' - network
        """
        if size_bytes == 0:
            return "0B"
        if units == 's':
            size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        elif units == 'n':
            size_name = ("Bps", "KBps", "MBps", "GBps")
        else:
            size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "{} {}".format(s, size_name[i])

    @staticmethod
    def message_constructor(status, message, keyboard=False, edit=False):
        '''
        :param status:
        :param message:
        :param keyboard: Default False
        :param edit:  Default False
        :return: JSON
        '''
        return {'status': status, 
                'message': message,
                'keyboard': keyboard,
                'edit': edit}

    def api_call(self, method, fields=None, ids=None, filename=None):
        headers = {'X-Transmission-Session-Id': self.session_id}
        params = {'method': method, 'arguments': {}}
        if fields:
            params['arguments']['fields'] = fields
        if ids:
            params['arguments']['ids'] = int(ids)
        if filename:
            params['arguments']['filename'] = filename
        request = post(cfg.url,
                       data=dumps(params),
                       headers=headers,
                       auth=(cfg.username, cfg.password),
                       verify=cfg.verify)
        return False if str(request.text).find('success') == -1 else request.text

    @staticmethod
    def result_parser(result):
        # try:
        obj = loads(result)
        if 'torrent-duplicate' in obj['arguments']:
            tmp_data = obj['arguments']['torrent-duplicate']['name']
            tmp_result = 'Already exist'
        elif 'torrent-added' in obj['arguments']:
            tmp_data = obj['arguments']['torrent-added']
            tmp_result = obj['result']
        elif 'torrents' in obj['arguments']:
            tmp_data = obj['arguments']['torrents']
            tmp_result = obj['result']
        else:
            tmp_data = obj['arguments']
            tmp_result = obj['result']
        return {'data': tmp_data, 'result': tmp_result}
        # except IndexError as err:
        #     return {'result': err}

    # GET ================================
    def get_all(self):
        result = self.api_call('torrent-get', fields=['id', 'name', 'status', 'comment',
                                                      'error', 'errorString', 'isFinished',
                                                      'leftUntilDone', 'percentDone',
                                                      'sizeWhenDone', 'startDate',
                                                      'uploadRatio', 'totalSize'])
        return self.result_parser(result)
    
    def get_all_short(self):
        result = self.api_call('torrent-get', fields=['id', 'errorString',
                                                      'isFinished',
                                                      'percentDone'])
        return self.result_parser(result)

    def get_by_id(self, t_id):
        '''
        :param t_id: Integer
        :return: List
        '''
        result = self.api_call('torrent-get', fields=['name', 'totalSize'], ids=t_id)
        return self.result_parser(result)

    def get_status(self):
        result = self.api_call('session-stats')
        parsed_result = self.result_parser(result)
        menu = status_inline_kbd()
        if parsed_result['result'] == 'success':
            data = parsed_result['data']
            f_str = cs.statusText.format(data['activeTorrentCount'],
                                         data['pausedTorrentCount'],
                                         data['torrentCount'],
                                         self.convert_sizes(data['downloadSpeed'], 'n'),
                                         self.convert_sizes(data['uploadSpeed'], 'n'),
                                         self.convert_sizes(data['cumulative-stats']['uploadedBytes'], 's'),
                                         self.convert_sizes(data['cumulative-stats']['downloadedBytes'], 's'))
            return self.message_constructor(True, f_str, menu)
        else:
            return self.message_constructor(False, 'Error on Getting Torrents')

    def get_all_torrents(self):
        result = self.api_call('torrent-get', fields=['id', 'name', 'status', 'errorString'])
        parsed_result = self.result_parser(result)
        torr_list = []
        if parsed_result['result'] == 'success':
            if parsed_result['data'][0]:
                for i in parsed_result['data']:
                    icon, state, keyboard = self.take_state(i, 'short')
                    f_str = cs.torrent_short.format(icon, i['name'], state)
                    torr_list.append(self.message_constructor(True, f_str, keyboard))
                return torr_list
            else:
                response = 'No Active Torrents'
                return [self.message_constructor(True, response)]
        else:
            return [self.message_constructor(False, 'Error on Getting Torrents')]

    def torrent_info(self, torr_id):
        result = self.api_call('torrent-get',
                               fields=['id', 'name', 'status', 'errorString',
                                       'addedDate', 'peers', 'totalSize',
                                       'rateDownload', 'rateUpload', 'uploadRatio'],
                               ids=torr_id)
        parsed_result = self.result_parser(result)
        if parsed_result['result'] == 'success':
            icon, state, keyboard = self.take_state(parsed_result['data'][0], 'full')
            data = parsed_result['data'][0]
            response = cs.getTorrInfo.format(icon, data['name'], state,
                                             self.timestamp_to_datetime(data['addedDate']),
                                             self.convert_sizes(data['rateDownload'], 'n'),
                                             self.convert_sizes(data['rateUpload'], 'n'),
                                             len(data['peers']),
                                             self.convert_sizes(data['totalSize'], 's'),
                                             )
            return [self.message_constructor(True, response, keyboard, True)]
        else:
            return [self.message_constructor(False, 'Error on Getting Torrent')]

    def get_short(self, torr_id):
        result = self.api_call('torrent-get', fields=['id', 'name', 'status', 'errorString'], ids=torr_id)
        parsed_result = self.result_parser(result)
        if parsed_result['result'] == 'success':
            data = parsed_result['data'][0]
            icon, state, keyboard = self.take_state(data, 'short')
            f_str = cs.torrent_short.format(icon, data['name'], state)
            torr = self.message_constructor(True, f_str, keyboard, True)
            return [torr]
        else:
            return [self.message_constructor(False, 'Error on Getting Torrents')]

    # ADD ================================
    def add_by_magnetlink(self, mglink):
        names = []
        trackers = []
        # try:
        for item in mglink.split('&'):
            decoded = unquote(item)
            if decoded.startswith('dn='):
                names.append(decoded.replace('dn=', ''))
            if decoded.startswith('tr='):
                trackers.append(decoded.replace('tr=', ''))

        name_str = ','.join(names)
        trackers_str = ','.join(trackers)

        result = self.api_call('torrent-add', filename=mglink)
        parsed_result = self.result_parser(result)

        if parsed_result['result'] == 'success':
            message = cs.ok.format(name_str, trackers_str)
            return self.message_constructor(True, message)
        else:
            message = f'{parsed_result["data"]}\n{parsed_result["result"]}'
            return self.message_constructor(False, message)
        # except Exception as e:
            # message = f'Bad Error! {e}'
            # return self.message_constructor(False, message)

    # SET =================================
    def start_all(self):
        result = self.api_call('torrent-start')
        if result:
            return [self.message_constructor(True, 'All Started')]
        else:
            return [self.message_constructor(False, 'Error on Starting Torrents')]

    def stop_all(self):
        result = self.api_call('torrent-stop')
        if result:
            return [self.message_constructor(True, 'All Stopped')]
        else:
            return [self.message_constructor(False, 'Error on Stopping Torrents')]

    def start_by_id(self, torr_id):
        self.api_call('torrent-start', ids=torr_id)
        time.sleep(1)
        result = self.api_call('torrent-get',
                               fields=['id', 'name', 'status', 'errorString',
                                       'addedDate', 'peers', 'totalSize',
                                       'rateDownload', 'rateUpload', 'uploadRatio'],
                               ids=torr_id)
        parsed_result = self.result_parser(result)
        if parsed_result['result'] == 'success':
            icon, state, keyboard = self.take_state(parsed_result['data'][0], 'full')
            data = parsed_result['data'][0]
            response = cs.getTorrInfo.format(icon, data['name'], state,
                                             self.timestamp_to_datetime(data['addedDate']),
                                             self.convert_sizes(data['rateDownload'], 'n'),
                                             self.convert_sizes(data['rateUpload'], 'n'),
                                             len(data['peers']),
                                             self.convert_sizes(data['totalSize'], 's'),
                                             )
            return [self.message_constructor(True, response, keyboard, True)]
        else:
            return [self.message_constructor(False, 'Error on Starting Torrent')]

    def stop_by_id(self, torr_id):
        self.api_call('torrent-stop', ids=torr_id)
        time.sleep(1)
        result = self.api_call('torrent-get',
                               fields=['id', 'name', 'status', 'errorString',
                                       'addedDate', 'peers', 'totalSize',
                                       'rateDownload', 'rateUpload', 'uploadRatio'],
                               ids=torr_id)
        parsed_result = self.result_parser(result)
        if parsed_result['result'] == 'success':
            icon, state, keyboard = self.take_state(parsed_result['data'][0], 'full')
            data = parsed_result['data'][0]
            response = cs.getTorrInfo.format(icon, data['name'], state,
                                             self.timestamp_to_datetime(data['addedDate']),
                                             self.convert_sizes(data['rateDownload'], 'n'),
                                             self.convert_sizes(data['rateUpload'], 'n'),
                                             len(data['peers']),
                                             self.convert_sizes(data['totalSize'], 's'),
                                             )
            return [self.message_constructor(True, response, keyboard, True)]
        else:
            return [self.message_constructor(False, 'Error on Stop Torrent')]

    def delete_by_id(self, torr_id):
        result = self.api_call('torrent-get', fields=['id', 'name', 'status', 'errorString'], ids=torr_id)
        parsed_result = self.result_parser(result)
        if parsed_result['result'] == 'success':
            data = parsed_result['data'][0]
            icon, state, keyboard = self.take_state(data, 'short')
            f_str = cs.torrent_short.format(icon, data['name'], state)
            torr = self.message_constructor(True, f_str, remove_torr_kbd(torr_id), True)
            return [torr]

    def delete_by_id_confirm(self, torr_id):
        result = self.api_call('torrent-remove', ids=torr_id)
        if result:
            return [self.message_constructor(True, 'Removed')]
        else:
            return [self.message_constructor(False, 'Error on Removing Torrents')]

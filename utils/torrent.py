"""
Module for control transmission daemon thru rpc
"""
import sys
import math
import datetime
from urllib.parse import unquote
from json import loads, dumps
from requests import get, post

from interface.keyboards import inline_kbd
import interface.strings as cs
import config as cfg

# python 3.6 not accept 0 as argument in fromtimestamp on Windows
EPOCH = datetime.datetime.utcfromtimestamp(0) if sys.platform == 'win32' else datetime.datetime.fromtimestamp(0)


def timedelta_to_seconds(delta):
    seconds = (delta.microseconds * 1e6) + delta.seconds + (delta.days * 86400)
    seconds = abs(seconds)

    return seconds


def timestamp_to_datetime(timestamp, epoch=EPOCH):
    epoch = datetime.datetime.fromordinal(epoch.toordinal())
    epoch_difference = timedelta_to_seconds(epoch - EPOCH)
    adjusted_timestamp = timestamp - epoch_difference
    date = datetime.datetime.fromtimestamp(adjusted_timestamp)
    return date


# units: 's' - storage, 'n' - network
def convert_size(size_bytes, units='s'):
    if size_bytes == 0:
        return "0B"
    if units == 's':
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    else:
        size_name = ("Bps", "KBps", "MBps", "GBps")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "{} {}".format(s, size_name[i])


def message_constructor(status, message, keyboard=False):
    return {'status': status, 
            'message': message,
            'keyboard': keyboard}


def get_session_id():
    sessionid_request = get(cfg.url,
                            auth=(cfg.username, cfg.password),
                            verify=cfg.verify)
    return sessionid_request.headers['x-transmission-session-id']


def constructor(method):
        headers = {'X-Transmission-Session-Id': get_session_id()}
        request = post(cfg.url,
                       data=dumps(method),
                       headers=headers,
                       auth=(cfg.username, cfg.password),
                       verify=cfg.verify)
        return False if str(request.text).find('success') == -1 \
                        else request.text


def add_by_magnetlink(mglink):
    names = []
    trackers = []
    try:
        for item in mglink.split('&'):
            decoded = unquote(item)
            if decoded.startswith('dn='):
                names.append(decoded.replace('dn=', ''))
            if decoded.startswith('tr='):
                trackers.append(decoded.replace('tr=', ''))

        nameStr = ','.join(names)
        trackersStr = ','.join(trackers)

        method = {'method': 'torrent-add', 'arguments': {
                  'filename': mglink}}
        result = constructor(method)
        if result:
            return message_constructor(True, cs.ok.format(nameStr,
                                                          trackersStr))
        else:
            message = 'Magnet Link: {}\nAnswer: {}'.format(mglink,
                                                           result.text)
            return message_constructor(False, message)
    except Exception as e:
        return message_constructor(False, 'Bad Error!  {}'.format(e))


def get_status():
    method = {'method': 'session-stats'}
    result = constructor(method)
    if result:
        dumped = loads(result)['arguments']
        fStr = cs.statusText.format(dumped['activeTorrentCount'],
                                    dumped['pausedTorrentCount'],
                                    dumped['torrentCount'],
                                    convert_size(dumped['downloadSpeed'], 'n'),
                                    convert_size(dumped['uploadSpeed'], 'n'),
                                    convert_size(dumped['cumulative-stats']['uploadedBytes'], 's'),
                                    convert_size(dumped['cumulative-stats']['downloadedBytes'], 's'))
        return message_constructor(True, fStr)
    else:
        return message_constructor(False, 'Error on Getting Torrents')


def start_all():
    method = {'method': 'torrent-start', 'arguments': {}}
    result = constructor(method)
    if result:
        return message_constructor(True, 'Started')
    else:
        return message_constructor(False, 'Error on Getting Torrents')


def start_by_id(torr_id):
    method = {'method': 'torrent-start', 'arguments': {
        'ids': int(torr_id)
    }}
    result = constructor(method)
    if result:
        return message_constructor(True, 'Started')
    else:
        return message_constructor(False, 'Error on Getting Torrents')


def stop_all():
    method = {'method': 'torrent-stop', 'arguments': {}}
    result = constructor(method)
    if result:
        return message_constructor(True, 'Stoped')
    else:
        return message_constructor(False, 'Error on Getting Torrents')


def stop_by_id(torr_id):
    method = {'method': 'torrent-stop', 'arguments': {
        'ids': int(torr_id)
    }}
    result = constructor(method)
    if result:
        return message_constructor(True, 'Stoped')
    else:
        return message_constructor(False, 'Error on Getting Torrents')


def delete_by_id(torr_id):
    method = {'method': 'torrent-remove', 'arguments': {
        'ids': int(torr_id)
    }}
    result = constructor(method)
    if result:
        return message_constructor(True, 'Deleted')
    else:
        return message_constructor(False, 'Error on Getting Torrents')


# TODO: Check if i don't have a torrents
def get_all_torrents():
    method = {
                'arguments': {
                    'fields': ['id', 'name', 'status']
                  },
                'method': 'torrent-get'
             }
    result = constructor(method)
    if result:
        tmp = loads(result)['arguments']['torrents']
        response = ''
        if tmp:
            for i in tmp:
                if i['status'] == 0:
                    status = 'Torrent is stopped'
                    menu = cs.stop
                elif i['status'] == 1:
                    status = 'Queued to check files'
                    menu = cs.start
                elif i['status'] == 2:
                    status = 'Checking files'
                    menu = cs.start
                elif i['status'] == 3:
                    status = 'Queued to download'
                    menu = cs.start
                elif i['status'] == 4:
                    status = 'Downloading'
                    menu = cs.start
                elif i['status'] == 5:
                    status = 'Queued to seed'
                    menu = cs.start
                else:
                    status = 'Seeding'
                    menu = cs.start
                response += cs.getLastAct.format(i['id'], i['name'], status, menu.format(i['id']))
        else:
            response = 'No Active Torrents'
        return message_constructor(True, response)
    else:
        return message_constructor(False, 'Error on Getting Torrents')


def torrent_info(torr_id):
    print(id)
    method = {
                'arguments': {
                    'fields': ['id', 'name', 'status',
                               'addedDate', 'peers', 'totalSize',
                               'rateDownload', 'rateUpload', 'uploadRatio'],
                    'ids': int(torr_id)
                  },
                'method': 'torrent-get'
             }
    result = loads(constructor(method))
    if result['arguments']['torrents'][0]:
        tmp = result['arguments']['torrents'][0]
        if tmp['status'] == 0:
            icon = '⏹️'
            status = 'Torrent is stopped'
            menu = inline_kbd(tmp['id'], 'stopped')
        elif tmp['status'] == 1:
            icon = '⏯️'
            status = 'Queued to check files'
            menu = inline_kbd(tmp['id'], 'stated')
        elif tmp['status'] == 2:
            icon = '▶️'
            status = 'Checking files'
            menu = inline_kbd(tmp['id'], 'stated')
        elif tmp['status'] == 3:
            icon = '⏯️'
            status = 'Queued to download'
            menu = inline_kbd(tmp['id'], 'stated')
        elif tmp['status'] == 4:
            icon = '▶️'
            status = 'Downloading'
            menu = inline_kbd(tmp['id'], 'stated')
        elif tmp['status'] == 5:
            icon = '⏯️'
            status = 'Queued to seed'
            menu = inline_kbd(tmp['id'], 'stated')
        else:
            icon = '▶️'
            status = 'Seeding'
            menu = inline_kbd(tmp['id'], 'stated')
        response = cs.getTorrInfo.format(icon, tmp['name'], status, '',
                                         convert_size(tmp['rateDownload'], 'n'),
                                         convert_size(tmp['rateUpload'], 'n'),
                                         len(tmp['peers']),
                                         convert_size(tmp['totalSize'], 's'),
                                         timestamp_to_datetime(tmp['addedDate']))
        return message_constructor(True, response, menu)
    else:
        return message_constructor(False, 'Error on Getting Torrent')

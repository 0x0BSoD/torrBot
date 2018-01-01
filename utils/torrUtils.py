from urllib.parse import unquote
from json import loads, dumps
from requests import get, post
import math
import datetime

import interface.strings as cs
import config as cfg
EPOCH = datetime.datetime.fromtimestamp(0)


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


# untits: 's' - storage, 'n' - network
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


def messageConstr(status, message):
    return {'status': status, 'message': message}


def getSessionId():
    sessionid_request = get(cfg.url,
                            auth=(cfg.username, cfg.password),
                            verify=cfg.verify)
    return sessionid_request.headers['x-transmission-session-id']


def constructor(method):
        headers = {'X-Transmission-Session-Id': getSessionId()}
        request = post(cfg.url,
                       data=dumps(method),
                       headers=headers,
                       auth=(cfg.username, cfg.password),
                       verify=cfg.verify)
        return False if str(request.text).find('success') == -1 \
                        else request.text


def addByMagnetlink(mglink):
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
            return messageConstr(True, cs.ok.format(nameStr,
                                                    trackersStr))
        else:
            message = 'Magnet Link: {}\nAnswer: {}'.format(mglink,
                                                           result.text)
            return messageConstr(False, message)
    except Exception as e:
        return messageConstr(False, 'Bad Error!  {}'.format(e))


def getStatus():
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
        return messageConstr(True, fStr)
    else:
        return messageConstr(False, 'Error on Getting Torrents')


def startAll():
    method = {'method': 'torrent-start', 'arguments': {}}
    result = constructor(method)
    if result:
        return messageConstr(True, 'Started')
    else:
        return messageConstr(False, 'Error on Getting Torrents')


def stopAll():
    method = {'method': 'torrent-stop', 'arguments': {}}
    result = constructor(method)
    if result:
        return messageConstr(True, 'Stoped')
    else:
        return messageConstr(False, 'Error on Getting Torrents')


def recentlyAct():
    method = {
                'arguments': {
                    'fields': ['id', 'name', 'status']
                  },
                'method': 'torrent-get'
             }
    result = constructor(method)
    if result:
        tmp = loads(result)['arguments']['torrents']
        ress = ''
        for i in tmp:
            if i['status'] == 0:
                status = 'Torrent is stopped'
            elif i['status'] == 1:
                status = 'Queued to check files'
            elif i['status'] == 2:
                status = 'Checking files'
            elif i['status'] == 3:
                status = 'Queued to download'
            elif i['status'] == 4:
                status = 'Downloading'
            elif i['status'] == 5:
                status = 'Queued to seed'
            elif i['status'] == 6:
                status = 'Seeding'
            ress += cs.getLastAct.format(i['id'], i['name'], status, ' ')
        return messageConstr(True, ress)
    else:
        return messageConstr(False, 'Error on Getting Torrents')


def torrInfo(id):
    method = {
                'arguments': {
                    'fields': ['id', 'name', 'status',
                               'addedDate', 'peers', 'totalSize',
                               'rateDownload', 'rateUpload', 'uploadRatio'],
                    'ids': int(id)
                  },
                'method': 'torrent-get'
             }
    result = loads(constructor(method))
    if result['arguments']['torrents'][0]:
        tmp = result['arguments']['torrents'][0]
        if tmp['status'] == 0:
            icon = '⏹️'
            status = 'Torrent is stopped'
        elif tmp['status'] == 1:
            icon = '⏯️'
            status = 'Queued to check files'
        elif tmp['status'] == 2:
            icon = '▶️'
            status = 'Checking files'
        elif tmp['status'] == 3:
            icon = '⏯️'
            status = 'Queued to download'
        elif tmp['status'] == 4:
            icon = '▶️'
            status = 'Downloading'
        elif tmp['status'] == 5:
            icon = '⏯️'
            status = 'Queued to seed'
        elif tmp['status'] == 6:
            icon = '▶️'
            status = 'Seeding'
        ress = cs.getTorrInfo.format(icon, tmp['name'], status, 'menu',
                                     convert_size(tmp['rateDownload'], 'n'),
                                     convert_size(tmp['rateUpload'], 'n'),
                                     len(tmp['peers']),
                                     convert_size(tmp['totalSize'], 's'),
                                     timestamp_to_datetime(tmp['addedDate']))
        return messageConstr(True, ress)
    else:
        return messageConstr(False, 'Error on Getting Torrent')

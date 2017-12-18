from urllib.parse import unquote
from json import loads, dumps
from requests import get, post
import math

import interface.strings as cs
import config as cfg


def convert_size_storage(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "{} {}".format(s, size_name[i])

def convert_size_speed(size_bytes):
   if size_bytes == 0:
       return "0B"
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
        print(request)
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
                  'filename': mglink } }
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
    print(result)
    if result:
        dumped = loads(result)['arguments']
        fStr = cs.statusText.format(dumped['activeTorrentCount'],
                                    dumped['pausedTorrentCount'],
                                    dumped['torrentCount'],
                                    convert_size_speed(dumped['downloadSpeed']),
                                    convert_size_speed(dumped['uploadSpeed']),
                                    convert_size_storage(dumped['cumulative-stats']['uploadedBytes']),
                                    convert_size_storage(dumped['cumulative-stats']['downloadedBytes']))
        return messageConstr(True, fStr)
    else:
        return messageConstr(False, 'Error on Getting Torrents')


def startAll():
    method = {'method': 'torrent-start', 'arguments': {
              'ids': 'all ids' }}
    result = constructor(method)
    print(result)
    if result:
        return messageConstr(True, 'Started')
    else:
        return messageConstr(False, 'Error on Getting Torrents')


def stopAll():
    method = {'method': 'torrent-stop', 'arguments': {
              'ids': 'all ids' }}
    result = constructor(method)
    print(result)
    if result:
        return messageConstr(True, 'Stoped')
    else:
        return messageConstr(False, 'Error on Getting Torrents')

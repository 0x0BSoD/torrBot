from urllib.parse import unquote
from json import dumps
from requests import get, post

import utils.strings as cs
import config as cfg


def messageConstr(status, message):
    return {"status": status, "message": message}


def getSessionId():
    sessionid_request = get(cfg.url,
                            auth=(cfg.username, cfg.password),
                            verify=cfg.verify)
    return sessionid_request.headers['x-transmission-session-id']


def constructor(method):
        headers = {"X-Transmission-Session-Id": getSessionId()}
        request = post(cfg.url,
                       data=dumps(method),
                       headers=headers,
                       auth=(cfg.username, cfg.password),
                       verify=cfg.verify)
        return False if str(request.text).find("success") == -1 \
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

        nameStr = ",".join(names)
        trackersStr = ",".join(trackers)

        method = {"method": "torrent-add", "arguments": {
                  "filename": mglink
                  }
                  }
        result = constructor(method)
        if result:
            return messageConstr(True, cs.ok.format(nameStr,
                                                    trackersStr))
        else:
            message = 'Magnet Link: {}\nAnswer: {}'.format(mglink,
                                                           result.text)
            return messageConstr(False, message)
    except Exception as e:
        return messageConstr(False, "Bad Error!  {}".format(e))


def getActiveTorrents():
    method = {"method": "torrent-get", "arguments": {
              "ids": "recently-active"
              }
              }
    result = constructor(method)
    if result:
        return messageConstr(True, result)
    else:
        return messageConstr(False, "Error on Getting Torrents")

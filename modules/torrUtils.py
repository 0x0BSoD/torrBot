from urllib.parse import unquote
from json import dumps
import requests

from modules import strings as cs
import config as cfg


def getSessionId():
    sessionid_request = requests.get(cfg.url,
                                     auth=(cfg.username,
                                           cfg.password),
                                     verify=False)
    return sessionid_request.headers['x-transmission-session-id']


def postLink(magnetlink):
    names = []
    trackers = []
    try:
        for item in magnetlink.split('&'):
            decoded = unquote(item)
            if decoded.startswith('dn='):
                names.append(decoded.replace('dn=', ''))
            if decoded.startswith('tr='):
                trackers.append(decoded.replace('tr=', ''))
        sessionid = getSessionId()
        headers = {"X-Transmission-Session-Id": sessionid}
        body = dumps({
                    "method": "torrent-add",
                    "arguments": {
                        "filename": magnetlink
                        }
                    })
        post_request = requests.post(cfg.url,
                                     data=body,
                                     headers=headers,
                                     auth=(cfg.username, cfg.password),
                                     verify=False)
        if str(post_request.text).find("success") == -1:
            message = 'Magnet Link: {}\nAnswer: {}'.format(magnetlink,
                                                           post_request.text)
            return {"status": False, "message": message}
        else:
            return {"status": True,
                    "message": cs.ok.format(",".join(names),
                                            ",".join(trackers))
                    }
    except Exception as e:
        return {"status": False, "message": e}


def getDownloading(magnetlink):
    names = []
    trackers = []
    try:
        for item in magnetlink.split('&'):
            decoded = unquote(item)
            if decoded.startswith('dn='):
                names.append(decoded.replace('dn=', ''))
            if decoded.startswith('tr='):
                trackers.append(decoded.replace('tr=', ''))
        sessionid = getSessionId()
        headers = {"X-Transmission-Session-Id": sessionid}
        body = dumps({
                    "method": "torrent-add",
                    "arguments": {
                        "filename": magnetlink
                        }
                    })
        post_request = requests.post(cfg.url,
                                     data=body,
                                     headers=headers,
                                     auth=(cfg.username, cfg.password),
                                     verify=False)
        if str(post_request.text).find("success") == -1:
            message = 'Magnet Link: {}\nAnswer: {}'.format(magnetlink,
                                                           post_request.text)
            return {"status": False, "message": message}
        else:
            return {"status": True,
                    "message": cs.ok.format(",".join(names),
                                            ",".join(trackers))
                    }
    except Exception as e:
        return {"status": False, "message": e}

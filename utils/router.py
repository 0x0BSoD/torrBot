from utils.torrUtils import addByMagnetlink, getStatus, startAll, stopAll
from utils.dirUtils import getFolderItems, fixRights
from utils.serverStatus import sysHealth, discFree


def parse(message):
    if message.startswith('magnet'):
        return addByMagnetlink(message)
    elif message.startswith('Get Status'):
        return getStatus()
    elif message.startswith('CPU'):
        return sysHealth()
    elif message.startswith('Free Space'):
        return discFree()
    elif message.startswith('chmod 777'):
        return fixRights()
    elif message.startswith('Dir Content'):
        return getFolderItems()
    elif message.startswith('Start All'):
        return startAll()
    elif message.startswith('Stop All'):
        return stopAll()
    else:
        return {"status": True,
                "message": "Don't get it (~ ~)"}

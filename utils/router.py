from utils.torrUtils import addByMagnetlink, getStatus, startAll, stopAll, recentlyAct, torrInfo
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
    elif message.startswith('Recently Active'):
        return recentlyAct()
    elif 'Info_' in message:
        try:
            id = message.split('_')
            return torrInfo(id[1])
        except Exception as e:
            return {"status": False,
                    "message": "Wrong ID"}
    else:
        return {"status": True,
                "message": "Don't get it (~ ~)"}

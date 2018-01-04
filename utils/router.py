from utils.torrUtils import addByMagnetlink, getStatus, startAll, stopAll, recentlyAct, torrInfo, startById, stopById, deleteById
from utils.dirUtils import getFolderItems, fixRights
from utils.serverStatus import sysHealth, discFree


def parseId(data):
    try:
        id = data.split('_')[1]
        return id
    except Exception as e:
        return {"status": False,
                "message": "Wrong ID"}


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
        return torrInfo(parseId(message))
    elif 'Stop_' in message:
        return stopById(parseId(message))
    elif 'Start_' in message:
        return startById(parseId(message))
    elif 'Delete_' in message:
        return deleteById(parseId(message))
    else:
        return {"status": True,
                "message": "Don't get it (~ ~)"}

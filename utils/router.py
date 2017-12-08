from utils.torrUtils import addByMagnetlink
from utils.dirUtils import getFolderItems, fixRights
from utils.serverStatus import sysHealth, discFree


def parse(message):
    if message.startswith('magnet'):
        return addByMagnetlink(message)
    # elif message.startswith('Show Downladed'):
    #     return getFolderItems()
    elif message.startswith('CPU'):
        return sysHealth()
    elif message.startswith('Free Space'):
        return discFree()
    elif message.startswith('chmod 777'):
        return fixRights()
    elif message.startswith('Dir Content'):
        return getFolderItems()
    else:
        return {"status": True,
                "message": "Don't get it (~ ~)"}
